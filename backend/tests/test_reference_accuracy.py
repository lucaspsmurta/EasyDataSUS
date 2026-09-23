import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pathlib import Path
from types import SimpleNamespace
import json

from backend.evaluation.catalog import catalog
from backend.evaluation.accuracy import compare_rows, cell_equal, limitation_matches, score, summarize, prepare, digest, validate_catalog, json_safe, write_new


class ReferenceAccuracyTests(unittest.TestCase):
    def test_column_rules_do_not_relax_identifiers_or_counts(self):
        rules = {'columns': {'0': {'normalization':'year'}, '2': {'absolute_tolerance':0.005}}}
        self.assertTrue(compare_rows([[2026,'031',12.864]],[['2026','031',12.86]],rules))
        self.assertFalse(compare_rows([[2026,'031',12.864]],[['2026',31,12.86]],rules))
        self.assertFalse(compare_rows([[10,12.864]],[[10.001,12.86]], {'columns':{'1':{'absolute_tolerance':0.005}}}))
        self.assertTrue(compare_rows([['pos_pcrflu',8190]],[['POS_PCRFLU',8190]],{'columns':{'0':{'normalization':'casefold'}}}))
        self.assertFalse(compare_rows([['pos_pcrflu',8190]],[['POS_PCRFLU',8190]],{}))

    def test_protocol_v3_ratio_and_repeated_cases(self):
        spec = catalog()
        self.assertEqual('reference-v3',spec['version'])
        c = {x['id']:x for x in spec['cases']}
        self.assertFalse(compare_rows([[0.6620176662]],[[0.6592319279]],c[5]['comparison']))
        self.assertTrue(compare_rows([[0.6620176662]],[[0.662018]],c[5]['comparison']))
        self.assertEqual(18,c[27]['repeat_of'])
        self.assertIn('365.25',c[42]['question'])
        self.assertIn('Na base de UBS',c[22]['question'])

    def test_shape_diagnostics_do_not_relax_accuracy(self):
        case = dict(expected_behavior="answer", expected_rows=[["F", 50.0]], comparison={})
        result = score(case, dict(success=True, data=[["F", 10, 50.0]]))
        self.assertFalse(result["result_correct"])
        self.assertEqual(["column_count_mismatch"], result["mismatch_reasons"])
        result = score(case, dict(success=True, data=[["F", 40.0]]))
        self.assertEqual(["values_or_order_mismatch"], result["mismatch_reasons"])

    def test_nonfinite_response_is_saved_without_becoming_null(self):
        data={"data":[[float("nan"),float("inf"),float("-inf"),None,0]]}
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/"result.json"
            write_new(p,data)
            restored=json.loads(p.read_text())
        self.assertEqual({"__nonfinite_number__":"NaN"},restored['data'][0][0])
        self.assertIsNone(restored['data'][0][3])
        self.assertEqual(0,restored['data'][0][4])
        self.assertFalse(compare_rows([[float('nan')]],[[float('nan')]],{}))
        self.assertFalse(compare_rows([[None]],[[float('nan')]],{}))
        self.assertFalse(compare_rows([[0]],[[float('inf')]],{}))

    def test_catalog_coverage(self):
        c=catalog()["cases"]
        self.assertEqual(set(range(1,69)),{x["id"] for x in c})
        self.assertEqual(64,sum(x["reference_sql"] is not None for x in c))
        self.assertEqual(4,sum(x["expected_behavior"]=="limitation" for x in c))
        self.assertTrue(all(x["review_status"]=="draft" for x in c))

    def test_unordered_multiset_not_set(self):
        self.assertTrue(compare_rows([["AC",2],["RJ",3]],[["RJ",3],["AC",2]],{}))
        self.assertFalse(compare_rows([[1],[1],[2]],[[1],[2],[2]],{}))

    def test_order_required(self):
        self.assertFalse(compare_rows([[1],[2]],[[2],[1]],{"ordered":True}))

    def test_null_identifiers_and_booleans(self):
        for a,b in [(None,0),("031",31),(True,1),("",None),(float("nan"),float("nan"))]:
            self.assertFalse(cell_equal(a,b))
        self.assertTrue(cell_equal(None,None))
        self.assertFalse(cell_equal(10000000000000001,10000000000000000))

    def test_rounding_tolerance(self):
        self.assertTrue(cell_equal(12.86,12.864,0.005))
        self.assertFalse(cell_equal(12.86,12.87,0.005))

    def test_tolerance_needs_bipartite_matching(self):
        # First expected row can match either candidate; second can match only the first.
        self.assertTrue(compare_rows([[0.0],[0.15]],[[0.1],[-0.1]],{"absolute_tolerance":0.11}))

    def test_empty_and_malformed(self):
        self.assertTrue(compare_rows([],[],{}))
        self.assertFalse(compare_rows([[1]],{"error":"db"},{}))
        self.assertFalse(compare_rows([[1]],[[1,2]],{}))

    def test_failure_in_denominator(self):
        case=dict(expected_behavior="answer",expected_rows=[[42]],comparison={})
        good=score(case,{"success":True,"data":[[42]]})
        bad=score(case,{"success":False})
        rows=[dict(expected_behavior="answer",assessment=a,response={"success":i==0}) for i,a in enumerate([good,bad])]
        report=summarize(rows)
        self.assertEqual(2,report["analytical_denominator"])
        self.assertEqual(0.5,report["execution_accuracy"])

    def test_successful_wrong_number_is_incorrect(self):
        case=dict(expected_behavior="answer",expected_rows=[[42]],comparison={})
        self.assertEqual("incorrect",score(case,{"success":True,"data":[[43]]})["status"])

    def test_limitation_is_not_generic_error(self):
        case=dict(expected_datasets=["leitos","surtos-srag"],expected_missing_data=["missing relation"])
        self.assertFalse(limitation_matches({"success":False,"data":{"error":"connection"}},case))
        response=dict(success=False,datasets=["surtos-srag","leitos"],relationships=[],
                      answerability=dict(answerable=False,reason="no relationship",missing_data=["missing relation"]),sql_generation_mode="none",
                      evaluation_metrics=dict(automatic_metrics=dict(failure_stage="answerability",query_executed=False)))
        self.assertTrue(limitation_matches(response,case))
        response["sql"]="SELECT 1"
        self.assertFalse(limitation_matches(response,case))

    def test_prepare_integrity_and_database_failures(self):
        spec=catalog()
        by_sql={c["reference_sql"]:c for c in spec["cases"] if c["reference_sql"]}
        class Client:
            fail=False
            def query(self,sql):
                if self.fail: raise RuntimeError("invalid reference SQL")
                c=by_sql[sql]
                return SimpleNamespace(column_names=c["columns"],column_types=["String"]*len(c["columns"]),result_rows=[])
        client=Client()
        snap={"table":{"fingerprint":[[10,1,2]]}}
        with TemporaryDirectory() as tmp, patch('backend.evaluation.accuracy.client_and_ask',return_value=(client,None)), patch('backend.evaluation.accuracy.snapshot',return_value=snap), patch('backend.evaluation.accuracy.ensure_readonly'):
            path=Path(tmp)/'gold.json'
            prepare(SimpleNamespace(catalog=None,output=path))
            bundle=json.loads(path.read_text(encoding='utf-8'))
            self.assertTrue(bundle['ready'])
            checksum=bundle.pop('integrity_sha256')
            self.assertEqual(checksum,digest(bundle))
            with self.assertRaises(FileExistsError): prepare(SimpleNamespace(catalog=None,output=path))
            client.fail=True
            bad=Path(tmp)/'bad.json'
            with self.assertRaises(RuntimeError): prepare(SimpleNamespace(catalog=None,output=bad))
            self.assertFalse(json.loads(bad.read_text())['ready'])

    def test_catalog_rejects_missing_or_duplicate_questions(self):
        spec=catalog()
        spec['cases'][-1]=spec['cases'][0]
        with self.assertRaises(ValueError): validate_catalog(spec)

    def test_prepare_rejects_changed_snapshot(self):
        spec=catalog()
        by_sql={c['reference_sql']:c for c in spec['cases'] if c['reference_sql']}
        client=SimpleNamespace(query=lambda sql:SimpleNamespace(column_names=by_sql[sql]['columns'],column_types=[],result_rows=[]))
        with TemporaryDirectory() as tmp, patch('backend.evaluation.accuracy.client_and_ask',return_value=(client,None)), patch('backend.evaluation.accuracy.ensure_readonly'), patch('backend.evaluation.accuracy.snapshot',side_effect=[{'t':{'fingerprint':[[10]]}},{'t':{'fingerprint':[[11]]}}]):
            p=Path(tmp)/'changed.json'
            with self.assertRaises(RuntimeError): prepare(SimpleNamespace(catalog=None,output=p))
            self.assertFalse(json.loads(p.read_text())['ready'])


if __name__=="__main__":
    unittest.main()
