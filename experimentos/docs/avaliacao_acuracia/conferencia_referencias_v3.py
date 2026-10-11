"""Recalcula as referências em Python, sem LLM e sem escrita no banco."""
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from math import isclose

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from backend.evaluation.accuracy import client_and_ask, snapshot, digest


def grouped(rows, keys, distinct=None, value=None):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    return [list(key) + [len({r[distinct] for r in group}) if distinct else
                         sum(r[value] for r in group) if value else len(group)]
            for key, group in groups.items()]


def extreme(rows, low=False):
    if not rows:
        return []
    target = (min if low else max)(r[-1] for r in rows)
    return [r for r in rows if r[-1] == target]


def ratio(a, b, scale=100):
    return a / b * scale if b else None


def same(left, right, ordered=False):
    def key(row):
        return tuple((type(v).__name__, str(v)) for v in row)
    if not ordered:
        left, right = sorted(left, key=key), sorted(right, key=key)
    if len(left) != len(right):
        return False
    for a, b in zip(left, right):
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                if isinstance(x, int) and isinstance(y, int):
                    if x != y:
                        return False
                elif not isclose(x, y, abs_tol=1e-9, rel_tol=1e-12):
                    return False
            elif x != y or type(x) != type(y):
                return False
    return True


def run():
    frozen = json.loads((ROOT / 'experimentos/referencias_68_catalogo_v3.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'docs/avaliacao_acuracia/catalogo_68_v3.json').read_text(encoding='utf-8'))
    client, _ = client_and_ask()
    before = snapshot(client)
    assert before == frozen['snapshot'], 'Os dados diferem do pacote v3.'
    assert digest(catalog) == frozen['catalog_sha256'], 'Catálogo diferente do pacote.'

    fields = {
        'vacinacao': 'paciente_idade paciente_enumSexoBiologico paciente_endereco_uf paciente_endereco_coIbgeMunicipio vacina_descricao_dose vacina_nome vacina_fabricante_nome vacina_dataAplicacao sistema_origem',
        'atencao_basica': 'cnes uf ibge bairro logradouro latitude longitude',
        'srag': 'dt_notific sem_not sg_uf_not co_mun_not nu_idade_n tp_idade hospital evolucao uti febre tosse garganta dispneia diarreia vomito cardiopati hematologi hepatica asma diabetes neurologic pneumopati imunodepre renal obesidade pcr_sars2 pos_pcrflu pcr_vsr',
        'leitos': 'COMP UF CO_IBGE REGIAO CNES TP_GESTAO DS_TIPO_UNIDADE NATUREZA_JURIDICA LEITOS_EXISTENTES LEITOS_SUS UTI_TOTAL_EXIST UTI_ADULTO_EXIST UTI_PEDIATRICO_EXIST UTI_NEONATAL_EXIST UTI_CORONARIANA_EXIST UTI_QUEIMADO_EXIST',
    }
    tables = {}
    for table, names in fields.items():
        columns = names.split()
        result = client.query('SELECT ' + ','.join(columns) + ' FROM ' + table)
        tables[table] = [dict(zip(columns, row)) for row in result.result_rows]
    v, u, s, beds = [tables[t] for t in fields]
    nonempty = lambda value: value is not None and value != ''
    validv = [r for r in v if nonempty(r['paciente_endereco_uf'])]
    positiveu = [r for r in u if r['cnes'] > 0]
    municipalu = [r for r in positiveu if r['ibge'] > 0]
    valids = [r for r in s if nonempty(r['sg_uf_not'])]
    latest = max(r['COMP'] for r in beds)
    b = [r for r in beds if r['COMP'] == latest]
    validb = [r for r in b if nonempty(r['UF'])]
    out = {}
    out[1] = [[len(v)]]
    out[2] = extreme(grouped([r for r in validv if r['vacina_descricao_dose'] == '1ª Dose'], ['paciente_endereco_uf']))
    out[3] = [[sum(r['vacina_descricao_dose'] == '2ª Dose' for r in v)]]
    doses = defaultdict(lambda: [0, 0])
    for r in validv:
        pair = doses[r['paciente_endereco_uf']]
        pair[0] += r['vacina_descricao_dose'] == '1ª Dose'
        pair[1] += r['vacina_descricao_dose'] == '2ª Dose'
    out[4] = [[uf, a-b] for uf, (a, b) in doses.items()]
    boost = [r for r in v if 'reforço' in (r['vacina_descricao_dose'] or '').lower()]
    out[5] = [[ratio(len(boost), sum(r['vacina_descricao_dose'] == '1ª Dose' for r in v), 1)]]
    sex = Counter(r['paciente_enumSexoBiologico'] for r in v)
    out[6] = [[gender, ratio(sex[gender], sex['F']+sex['M'])] for gender in ['F','M']]
    ages = [dict(r, faixa='0-18' if r['paciente_idade'] < 19 else '19-59' if r['paciente_idade'] < 60 else '60+') for r in v if r['paciente_idade'] >= 0]
    out[7] = extreme(grouped(ages, ['faixa']), True)
    out[8] = extreme(grouped([r for r in validv if nonempty(r['paciente_endereco_coIbgeMunicipio'])], ['paciente_endereco_uf', 'paciente_endereco_coIbgeMunicipio']))
    out[9] = grouped([r for r in ages if nonempty(r['paciente_endereco_uf'])], ['paciente_endereco_uf','faixa'])
    out[10] = grouped(v, ['sistema_origem'])
    out[11] = extreme([[name, ratio(n,len(v))] for name,n in grouped([r for r in v if nonempty(r['vacina_nome'])], ['vacina_nome'])])
    out[12] = extreme(grouped([r for r in v if nonempty(r['vacina_fabricante_nome'])], ['vacina_fabricante_nome']))
    months = [dict(r, mes=r['vacina_dataAplicacao'].strftime('%Y-%m')) for r in v if r['vacina_dataAplicacao'] is not None]
    out[13] = grouped(months, ['mes'])
    out[14] = extreme(grouped([r for r in months if nonempty(r['paciente_endereco_uf'])], ['paciente_endereco_uf','mes']))
    out[15] = grouped(boost, ['vacina_descricao_dose'])
    out[16] = [[len({r['cnes'] for r in positiveu})]]
    out[17] = out[26] = grouped(positiveu, ['uf'], distinct='cnes')
    out[18] = out[27] = extreme(out[17])
    out[19] = [[len({r['ibge'] for r in municipalu})]]
    municipal_counts = grouped(municipalu, ['ibge'], distinct='cnes')
    out[20] = out[21] = extreme(municipal_counts)
    out[30] = extreme(municipal_counts, True)
    out[22] = grouped([r for r in municipalu if 21 <= r['uf'] <= 29], ['ibge'], distinct='cnes')
    coords = [r for r in positiveu if r['latitude'] != 0 and r['longitude'] != 0 and -90 <= r['latitude'] <= 90 and -180 <= r['longitude'] <= 180]
    out[23] = [[len({r['cnes'] for r in coords})]]
    out[24] = extreme(grouped([r for r in coords if r['ibge']>0], ['ibge'], distinct='cnes'))
    out[25] = grouped([r for r in municipalu if r['bairro'].strip()], ['uf','ibge','bairro'], distinct='cnes')
    out[28] = [[len({r['cnes'] for r in positiveu if r['logradouro'].strip() and r['bairro'].strip()})]]
    out[29] = grouped([r for r in positiveu if r['ibge']==355030], ['bairro'], distinct='cnes')
    out[31] = [[len(s)]]
    out[32] = grouped([dict(r, ano=r['dt_notific'].year) for r in s if r['dt_notific'] != date(1970,1,1)], ['ano','sem_not'])
    out[33] = extreme(grouped(valids, ['sg_uf_not']))
    out[34] = grouped(valids, ['sg_uf_not'])
    out[35] = [[len({r['co_mun_not'] for r in s if r['co_mun_not']>0})]]
    hospital = [r for r in s if r['hospital']==1]
    out[36] = [[ratio(len(hospital),len(s))]]
    out[37] = [[sum(r['evolucao']==2 for r in s)]]
    out[38] = [[ratio(sum(r['evolucao']==2 for r in hospital),len(hospital))]]
    out[39] = [[ratio(sum(r['uti']==1 for r in s),len(s))]]
    totals = Counter(r['sg_uf_not'] for r in valids)
    deaths = Counter(r['sg_uf_not'] for r in valids if r['evolucao']==2)
    out[40] = extreme([[uf,ratio(deaths[uf],n)] for uf,n in totals.items()])
    out[41] = [[sum(r[k]==1 for r in s) for k in 'febre tosse garganta dispneia diarreia vomito'.split()]]
    age_counts = Counter()
    for r in s:
        age, unit = r['nu_idade_n'], r['tp_idade']
        if age is None or age<0 or unit not in (1,2,3):
            continue
        years = age / {1:365.25,2:12,3:1}[unit]
        age_counts['0-18' if years<19 else '19-59' if years<60 else '60+'] += 1
    out[42] = extreme([list(pair) for pair in age_counts.items()])
    indicators = 'cardiopati hematologi hepatica asma diabetes neurologic pneumopati imunodepre renal obesidade'.split()
    out[43] = [[ratio(sum(any(r[k]==1 for k in indicators) for r in s),len(s))]]
    out[44] = [[sum(r['pcr_sars2']==1 or r['pos_pcrflu']==1 for r in s)]]
    out[45] = extreme([[k,sum(r[k]==1 for r in s)] for k in ['pcr_sars2','pos_pcrflu','pcr_vsr']])
    for i, k in [(46,'LEITOS_EXISTENTES'),(47,'LEITOS_SUS'),(51,'UTI_TOTAL_EXIST')]:
        out[i] = [[sum(r[k] for r in b)]]
    for i,k in [(48,'LEITOS_SUS'),(52,'UTI_TOTAL_EXIST')]:
        out[i] = [[ratio(sum(r[k] for r in b),sum(r['LEITOS_EXISTENTES'] for r in b))]]
    out[50] = grouped(validb, ['UF'], value='LEITOS_EXISTENTES')
    out[49] = extreme(out[50])
    out[53] = extreme(grouped([r for r in b if nonempty(r['DS_TIPO_UNIDADE'])], ['DS_TIPO_UNIDADE'], value='LEITOS_EXISTENTES'))
    out[54] = [[sum(r[k] for r in b) for k in 'UTI_ADULTO_EXIST UTI_PEDIATRICO_EXIST UTI_NEONATAL_EXIST UTI_CORONARIANA_EXIST UTI_QUEIMADO_EXIST'.split()]]
    out[55] = extreme(grouped(validb, ['UF'], value='UTI_NEONATAL_EXIST'),True)
    out[56] = extreme(grouped([r for r in b if nonempty(r['TP_GESTAO']) and nonempty(r['CNES'])], ['TP_GESTAO'],distinct='CNES'))
    out[57] = [[sum(r['LEITOS_SUS'] for r in b if (r['NATUREZA_JURIDICA'] or '').strip().startswith(('2','3')))]]
    sus_by_uf = dict(grouped(validb,['UF'],value='LEITOS_SUS'))
    out[58] = extreme([[uf,ratio(sus_by_uf[uf],n)] for uf,n in out[50] if n!=0])
    regionb = [r for r in b if nonempty(r['REGIAO'])]
    sus_by_region = dict(grouped(regionb,['REGIAO'],value='LEITOS_SUS'))
    out[59] = [[region,n,sus_by_region[region]] for region,n in grouped(regionb,['REGIAO'],value='LEITOS_EXISTENTES')]
    out[60] = extreme(grouped([r for r in validb if nonempty(r['CO_IBGE'])], ['UF','CO_IBGE'],value='LEITOS_EXISTENTES'))
    sm = Counter(r['co_mun_not'] for r in s if r['co_mun_not']>0)
    um = dict(municipal_counts)
    common = sm.keys() & um.keys()
    out[61] = [[len(common)]]
    out[62] = sorted([[m,sm[m],um[m]] for m in common],key=lambda row:(-row[1],row[0]))
    vc = Counter(r['paciente_endereco_uf'] for r in validv)
    bc = dict(grouped(validb,['UF'],value='UTI_TOTAL_EXIST'))
    out[63] = out[64] = [[uf,vc[uf],bc[uf]] for uf in vc.keys() & bc.keys() if bc[uf]>0]
    assert set(out) == set(range(1,65))
    checks=[]
    for c in sorted(frozen['cases'],key=lambda item:item['id']):
        i=c['id']
        if i>64:
            checks.append(dict(id=i,numeric_reference=False))
            continue
        current = client.query(c['reference_sql']).result_rows
        current = [list(row) for row in current]
        check = dict(id=i,sql_executed=True,
                     frozen_matches_current=same(c['expected_rows'],current,c['comparison']['ordered']),
                     python_matches_current=same(out[i],current,c['comparison']['ordered']),
                     row_count=len(current),column_count=len(c['columns']))
        checks.append(check)
        print(i,check['frozen_matches_current'],check['python_matches_current'])
    after=snapshot(client)
    quality={
        'ubs_nonpositive_uf':sum(r['uf']<=0 for r in positiveu),
        'q25_rows_with_invalid_municipality_and_nonempty_neighborhood':sum(r['ibge']<=0 and bool(r['bairro'].strip()) for r in positiveu),
        'bed_negative_values':{k:sum(r[k]<0 for r in b) for k in ['LEITOS_EXISTENTES','LEITOS_SUS']},
        'latest_comp':latest,
        'competences':sorted({r['COMP'] for r in beds}),
        'invalid_comp_format':sum(len(r['COMP'])!=6 or not r['COMP'].isdigit() or not 1<=int(r['COMP'][-2:])<=12 for r in beds),
        'duplicate_bed_cnes_latest':len(b)-len({r['CNES'] for r in b}),
        'srag_age_zero_with_known_unit':sum(r['nu_idade_n']==0 and r['tp_idade'] in (1,2,3) for r in s),
        'srag_unknown_age_unit':sum(r['tp_idade'] not in (1,2,3) for r in s),
        'vaccination_age_zero':sum(r['paciente_idade']==0 for r in v),
    }
    report=dict(created_at=datetime.now(timezone.utc).isoformat(),review_type='automated_technical_crosscheck_not_human_signoff',
                reference_sha256=frozen['integrity_sha256'],catalog_sha256=frozen['catalog_sha256'],
                snapshot_matches_frozen=before==frozen['snapshot'],snapshot_unchanged=before==after,
                comparison='Python independente; inteiros exatos; floats abs_tol=1e-9 e rel_tol=1e-12; sem normalização de saída',
                checks=checks,data_quality=quality)
    path=ROOT/'docs/avaliacao_acuracia/conferencia_referencias_v3_resultado.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(quality,ensure_ascii=True))
    print('Saved',path)


if __name__=='__main__':
    run()
