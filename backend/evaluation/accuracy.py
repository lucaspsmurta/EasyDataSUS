"""Prepare references and evaluate results: python -m backend.evaluation.accuracy --help."""
import argparse
from collections import Counter
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
import math
import re
from pathlib import Path
import sys
import time

from .catalog import ROOT, catalog

TABLES = ("vacinacao", "atencao_basica", "srag", "leitos")


def serial(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    raise TypeError(type(value).__name__)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=serial).encode()).hexdigest()


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(json_safe(data), f, ensure_ascii=False, indent=2, default=serial, allow_nan=False)


def json_safe(value):
    """Preserve undefined numbers explicitly, never conflate them with SQL NULL."""
    if isinstance(value, float) and not math.isfinite(value):
        return {"__nonfinite_number__": "NaN" if math.isnan(value) else ("Infinity" if value > 0 else "-Infinity")}
    if isinstance(value, Decimal) and not value.is_finite():
        return {"__nonfinite_number__": str(value)}
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


def has_nonfinite(value):
    if isinstance(value, (float, Decimal)):
        return not math.isfinite(value)
    if isinstance(value, dict):
        return "__nonfinite_number__" in value or any(has_nonfinite(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(has_nonfinite(v) for v in value)
    return False


def number(v):
    return isinstance(v, (int, float, Decimal)) and not isinstance(v, bool)


def cell_equal(a, b, absolute_tolerance=0.005, relative_tolerance=0.0):
    # Never coerce identifiers like '031' into numbers, or null into zero.
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if number(a) and number(b):
        if not math.isfinite(float(a)) or not math.isfinite(float(b)):
            return False
        if isinstance(a, int) and isinstance(b, int):
            return a == b
        return abs(Decimal(str(a))-Decimal(str(b))) <= max(
            Decimal(str(absolute_tolerance)), Decimal(str(relative_tolerance))*abs(Decimal(str(a))))
    return type(a) is type(b) and a == b


def compare_rows(expected, actual, rule):
    """Column-position contract; unordered MULTISET with one-to-one tolerant matching."""
    if has_nonfinite(expected) or has_nonfinite(actual):
        return False
    if not isinstance(actual, (list, tuple)):
        return False
    if len(expected) != len(actual):
        return False
    def normalized(value, policy):
        if policy == 'year' and isinstance(value, str) and re.fullmatch(r'[1-9][0-9]{3}', value):
            return int(value)
        if policy == 'casefold' and isinstance(value, str):
            return value.casefold()
        return value
    def same_cell(x, y, index):
        policy = dict(rule, **rule.get('columns', {}).get(str(index), {}))
        return cell_equal(normalized(x, policy.get('normalization')), normalized(y, policy.get('normalization')),
                          policy.get('absolute_tolerance', 0), policy.get('relative_tolerance', 0))
    def same(a, b):
        return isinstance(b, (list, tuple)) and len(a)==len(b) and all(
            same_cell(x,y,index) for index,(x,y) in enumerate(zip(a,b)))
    if rule.get("ordered"):
        return all(same(a,b) for a,b in zip(expected,actual))
    # Remove exact matches first so large exact result sets avoid quadratic matching.
    def key(row):
        return json.dumps(row, ensure_ascii=False, default=serial, sort_keys=True)
    counts = Counter(key(r) for r in actual)
    remaining=[]
    for row in expected:
        k=key(row)
        if counts[k]: counts[k]-=1
        else: remaining.append(row)
    candidates=[]
    for row in actual:
        k=key(row)
        if counts[k]:
            candidates.append(row)
            counts[k]-=1
    # Augmenting paths, not greedy matching: tolerances can create overlapping matches.
    adjacency=[[j for j,b in enumerate(candidates) if same(a,b)] for a in remaining]
    matched={}
    def augment(i, seen):
        for j in adjacency[i]:
            if j in seen: continue
            seen.add(j)
            if j not in matched or augment(matched[j],seen):
                matched[j]=i
                return True
        return False
    return all(augment(i,set()) for i in range(len(remaining)))


def limitation_matches(response, case):
    """A generic DB failure is NOT a correct controlled limitation."""
    answerability=response.get("answerability") or {}
    metrics=(response.get("evaluation_metrics") or {}).get("automatic_metrics") or {}
    return (response.get("success") is False
            and answerability.get("answerable") is False
            and bool(answerability.get("reason"))
            and set(case.get("expected_missing_data",[])).issubset(set(answerability.get("missing_data") or []))
            and metrics.get("failure_stage")=="answerability"
            and metrics.get("query_executed") is False
            and not response.get("sql")
            and response.get("sql_generation_mode")=="none"
            and set(response.get("datasets") or [])==set(case["expected_datasets"])
            and not response.get("relationships"))


def score(case, response):
    if case["expected_behavior"]=="unresolved":
        return dict(status="reference_pending", result_correct=None)
    if case["expected_behavior"]=="limitation":
        ok=limitation_matches(response,case)
        return dict(status="expected_limitation" if ok else "unexpected_behavior",
                    result_correct=None, limitation_correct=ok)
    if not response.get("success"):
        return dict(status="technical_failure", result_correct=False)
    expected, actual = case["expected_rows"], response.get("data")
    ok=compare_rows(expected,actual,case["comparison"])
    # Diagnostic only: never relax the score after observing a mismatch.
    reasons = []
    if not isinstance(actual, (list, tuple)):
        reasons.append("invalid_result_shape")
    else:
        if has_nonfinite(actual):
            reasons.append("nonfinite_result")
        if len(actual) != len(expected):
            reasons.append("row_count_mismatch")
        widths = {len(row) for row in expected}
        if widths and any(not isinstance(row, (list, tuple)) or len(row) not in widths for row in actual):
            reasons.append("column_count_mismatch")
        if not ok and not reasons:
            reasons.append("values_or_order_mismatch")
    return dict(status="correct" if ok else "incorrect", result_correct=ok,
                mismatch_reasons=reasons,
                expected_row_count=len(case["expected_rows"]),
                actual_row_count=len(response["data"]) if isinstance(response.get("data"),list) else None)


def summarize(results):
    analytical=[r for r in results if r["expected_behavior"]=="answer"]
    limitations=[r for r in results if r["expected_behavior"]=="limitation"]
    correct=sum(r["assessment"].get("result_correct") is True for r in analytical)
    operational=sum(r.get("response",{}).get("success") is True for r in analytical)
    def ratio(n,d): return n/d if d else None
    def selection(field, expected_field, rows):
        tp=fp=fn=0
        for r in rows:
            actual=set(r.get("response",{}).get(field) or [])
            expected=set(r.get(expected_field) or [])
            tp+=len(actual & expected)
            fp+=len(actual-expected)
            fn+=len(expected-actual)
        return dict(evaluated=len(rows),tp=tp,fp=fp,fn=fn,
                    precision=ratio(tp,tp+fp),recall=ratio(tp,tp+fn),f1=ratio(2*tp,2*tp+fp+fn))
    return dict(total=len(results), analytical_denominator=len(analytical), correct=correct,
                execution_accuracy=ratio(correct,len(analytical)),
                operational_successes=operational, operational_success_rate=ratio(operational,len(analytical)),
                limitation_denominator=len(limitations),
                limitations_correct=sum(r["assessment"].get("limitation_correct") is True for r in limitations),
                reference_pending=sum(r["expected_behavior"]=="unresolved" for r in results),
                statuses=dict(Counter(r["assessment"]["status"] for r in results)),
                dataset_selection=selection("datasets","expected_datasets",[r for r in results if r.get("expected_datasets")]),
                relationship_selection=selection("relationships","expected_relationships",[r for r in results if r.get("expected_relationships")]),
                response_fidelity=None,
                mismatch_reasons=dict(Counter(reason for r in analytical
                    for reason in r["assessment"].get("mismatch_reasons", []))))


def validate_catalog(spec):
    cases=spec["cases"]
    if len(cases)!=68 or {c["id"] for c in cases}!=set(range(1,69)):
        raise ValueError("Catalog must contain each of the 68 IDs exactly once")
    for c in cases:
        if not c.get("question") or c["expected_behavior"] not in {"answer","limitation","unresolved"}:
            raise ValueError(f"Invalid question/behavior: {c['id']}")
        if c["expected_behavior"]=="answer" and (not c.get("reference_sql") or not c.get("columns")):
            raise ValueError(f"Missing reference: {c['id']}")


def client_and_ask(need_ask=False):
    sys.path.insert(0,str(ROOT/"backend"))
    from dotenv import load_dotenv
    load_dotenv(ROOT/"backend/.env")
    from db.clickhouse import get_client
    if not need_ask:
        return get_client(),None
    from routes.query import ask, AskRequest
    from services.generation_diagnostics import capture
    def call(question,model):
        # No dataset supplied: evaluate routing for all questions.
        with capture() as diagnostics:
            response = ask(AskRequest(question=question,model=model))
        response['generation_diagnostics'] = diagnostics
        return response
    return get_client(),call


def snapshot(client):
    """Schema + order-independent content fingerprints, without exporting patient rows."""
    result={}
    for table in TABLES:
        schema=client.query(f"DESCRIBE TABLE {table}").result_rows
        columns=",".join('`'+r[0].replace('`','``')+'`' for r in schema)
        # JSON preserves NULLs and avoids nullable-tuple hashing errors in ClickHouse 24.3.
        row_hash=f"cityHash64(toJSONString(tuple({columns})))"
        stats=client.query(f"SELECT count(), groupBitXor({row_hash}), sum({row_hash}) FROM {table}").result_rows
        result[table]=dict(schema=[list(r[:2]) for r in schema],fingerprint=stats)
    return json.loads(json.dumps(result,default=serial))


def ensure_readonly(sql):
    import sqlglot
    from sqlglot import exp
    statements=sqlglot.parse(sql,read="clickhouse")
    if len(statements)!=1 or not isinstance(statements[0],exp.Query):
        raise ValueError("Reference must be a single SELECT/WITH query")
    if any(t.name not in TABLES and t.name not in {c.alias for c in statements[0].find_all(exp.CTE)}
           for t in statements[0].find_all(exp.Table)):
        raise ValueError("Unknown table in reference")


def prepare(args):
    if Path(args.output).exists(): raise FileExistsError(args.output)
    spec=json.loads(Path(args.catalog).read_text(encoding="utf-8")) if args.catalog else catalog()
    validate_catalog(spec)
    client,_=client_and_ask()
    before=snapshot(client)
    if any(not x["fingerprint"][0][0] for x in before.values()):
        raise ValueError("Empty table: load all datasets before preparing references")
    frozen=[]
    errors=[]
    for case in spec["cases"]:
        c=dict(case)
        if c["expected_behavior"]=="answer":
            try:
                ensure_readonly(c["reference_sql"])
                result=client.query(c["reference_sql"])
                if has_nonfinite(result.result_rows):
                    raise ValueError("Reference returned NaN/Infinity; fix undefined arithmetic before evaluation")
                # clickhouse-connect 0.6.x may omit metadata for valid empty results.
                if len(result.column_names)!=len(c["columns"]) and (result.result_rows or result.column_names):
                    raise ValueError("Reference column count differs from contract")
                c["expected_rows"]=result.result_rows
                c["reference_column_types"]=[str(t) for t in result.column_types]
            except Exception as exc:
                errors.append(dict(id=c["id"],error=str(exc)))
        frozen.append(c)
    after=snapshot(client)
    output=dict(version=spec["version"],created_at=datetime.now(timezone.utc).isoformat(),
                catalog_sha256=digest(spec),snapshot=before,snapshot_after=after,
                global_specification=spec["global_specification"],cases=frozen,
                errors=errors,ready=not errors and before==after)
    output["integrity_sha256"]=digest(output)
    write_new(args.output,output)
    if not output["ready"]:
        raise RuntimeError("References not ready: SQL errors or data changed; inspect output")
    print(f"References saved: {args.output}. Semantic review is separate from SQL execution.")


def run(args):
    import os
    if Path(args.output).exists(): raise FileExistsError(args.output)
    progress_path=Path(str(args.output)+".partial.json")
    if progress_path.exists(): raise FileExistsError(progress_path)
    bundle=json.loads(Path(args.references).read_text(encoding="utf-8"))
    checksum=bundle.pop("integrity_sha256",None)
    if not checksum or digest(bundle)!=checksum or not bundle.get("ready"):
        raise ValueError("Invalid/incomplete reference bundle; prepare again")
    cases=[c for c in bundle["cases"] if args.start<=c["id"]<=args.end]
    if not cases: raise ValueError("No selected questions")
    reviewed=all(c.get("review_status")=="reviewed" and c.get("reviewer") and c.get("reviewed_at")
                 for c in cases if c["expected_behavior"]!="unresolved")
    if not reviewed and not args.allow_draft:
        raise ValueError("Draft references. Use --allow-draft for exploratory runs; do not report as validated gold.")
    os.environ["SQL_GENERATION_STRATEGY"]=args.generation_strategy
    client,ask=client_and_ask(True)
    from llm.router import get_model_identifier
    import requests
    resolved_model=get_model_identifier(args.model)
    tags=requests.get(os.getenv("OLLAMA_HOST","http://localhost:11434").rstrip("/")+"/api/tags",timeout=10)
    tags.raise_for_status()
    if resolved_model not in {m.get("name") for m in tags.json().get("models",[])}:
        raise ValueError(f"Model unavailable: {resolved_model}")
    before=snapshot(client)
    if before!=bundle["snapshot"]: raise ValueError("Data/schema differs from reference snapshot")
    results=[]
    output=dict(reference_sha256=checksum,model=args.model,resolved_model=resolved_model,strategy=args.generation_strategy,
                started_at=datetime.now(timezone.utc).isoformat(),reference_reviewed=reviewed,
                valid_for_claims=False,results=results)
    write_new(progress_path,output)
    for case in cases:
        if case["expected_behavior"]=="unresolved":
            response={}
            elapsed=0
        else:
            start=time.monotonic()
            try:
                response=ask(case["question"],args.model)
                if not isinstance(response,dict): raise ValueError("Invalid endpoint result")
            except Exception as exc:
                response=dict(success=False,error=str(exc))
            elapsed=time.monotonic()-start
        assessment=score(case,response)
        results.append(dict(id=case["id"],question=case["question"],
                            expected_datasets=case["expected_datasets"],
                            expected_relationships=case["expected_relationships"],
                            expected_behavior=case["expected_behavior"],assessment=assessment,
                            dataset_selection_exact_match=(set(response.get("datasets") or [])==set(case["expected_datasets"])) if response else None,
                            relationship_selection_exact_match=(set(response.get("relationships") or [])==set(case["expected_relationships"])) if response else None,
                            elapsed_seconds=elapsed,response=response))
        print(f"Q{case['id']:02}: {assessment['status']}",flush=True)
        # This path was exclusively created by this run. Keep provisional results on interruption.
        progress_path.write_text(json.dumps(json_safe(output),ensure_ascii=False,indent=2,default=serial,allow_nan=False),encoding="utf-8")
    try:
        output["snapshot_after"]=snapshot(client)
        output["snapshot_unchanged"]=output["snapshot_after"]==before
    except Exception as exc:
        output["snapshot_unchanged"]=False
        output["snapshot_error"]=str(exc)
    output["summary"]=summarize(results)
    output["valid_for_claims"]=reviewed and output["snapshot_unchanged"]
    if not output["snapshot_unchanged"]:
        output["summary"]["execution_accuracy"]=None
    write_new(args.output,output)
    print(json.dumps(output["summary"],ensure_ascii=False,indent=2))
    if not output["snapshot_unchanged"]: raise RuntimeError("Run invalid: data changed or snapshot check failed")


def export(args):
    data=catalog()
    write_new(args.output,data)
    print(f"Catalog saved: {args.output}")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("export",help="Export all 68 specifications for human review")
    p.add_argument("--output",required=True)
    p.set_defaults(func=export)
    p=sub.add_parser("prepare",help="Execute reference SQL only, no LLM or data mutations")
    p.add_argument("--catalog")
    p.add_argument("--output",required=True)
    p.set_defaults(func=prepare)
    p=sub.add_parser("run",help="Run system and compare complete results with frozen references")
    p.add_argument("--references",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--model",default="qwen2.5-coder:7b")
    p.add_argument("--generation-strategy",choices=["llm_first","deterministic_first"],default="llm_first")
    p.add_argument("--start",type=int,default=1)
    p.add_argument("--end",type=int,default=68)
    p.add_argument("--allow-draft",action="store_true")
    p.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)


if __name__=="__main__":
    main()
