#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import csv, hashlib, json, math, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def fail(x): errors.append(x)
# features
rows=[]
for line in (ROOT/'data/features/scene_features.jsonl').read_text(encoding='utf-8').splitlines():
    if line.strip(): rows.append(json.loads(line))
if len(rows)!=938: fail(f'feature rows={len(rows)} != 938')
if len({(r['film_id'],r['scene_id']) for r in rows})!=938: fail('feature film/scene keys not unique')
features=['pacing','dialogue_density','action_density','character_interaction','emotion_intensity']
for r in rows:
    if r.get('measurement_status')!='measured': fail(f'non-measured feature row {r.get("film_id")}/{r.get("scene_id")}')
    for k in features:
        v=r.get(k)
        if not isinstance(v,(int,float)) or not math.isfinite(v) or not (0<=v<=1): fail(f'invalid feature {k} in {r.get("film_id")}/{r.get("scene_id")}')
# taskset
t=json.loads((ROOT/'data/taskset_v5/taskset.json').read_text())
if len(t['tasks'])!=240: fail('task count != 240')
if len({x['task_id'] for x in t['tasks']})!=240: fail('task ids not unique')
if len(t['base_intervals'])!=48: fail('base interval count != 48')
pairs={x['pair_key'] for x in t['base_intervals']}
if len(pairs)!=24: fail('directed pair count != 24')
if len({tuple(sorted(x.split('->'))) for x in pairs})!=12: fail('unordered pair count != 12')
if Counter(x['feature_axis'] for x in t['tasks']) != Counter({k:48 for k in features}): fail('feature balance mismatch')
if Counter(x['interval_type'] for x in t['tasks']) != Counter({'short':80,'medium':80,'long':80}): fail('interval balance mismatch')
# provenance
with (ROOT/'metadata/source_provenance.csv').open(encoding='utf-8') as f: prov=list(csv.DictReader(f))
if len(prov)!=10 or sum(int(x['cleaned_scene_count']) for x in prov)!=938 or sum(int(x['source_scene_count']) for x in prov)!=1101: fail('provenance counts mismatch')
# privacy scan (historical GitHub paths containing script.json are expected; machine-local paths are not)
for p in ROOT.rglob('*'):
    if p.is_file() and p.name!='SHA256SUMS' and p.suffix.lower() not in {'.zip'}:
        try: txt=p.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        for bad in ['/home/'+'alp-emre','127.'+'0.0.1','local'+'host:','/mnt/data/'+'dataset_audit']:
            if bad in txt: fail(f'forbidden private/local token {bad!r} in {p.relative_to(ROOT)}')
# checksums
sumfile=ROOT/'checksums/SHA256SUMS'
for line in sumfile.read_text().splitlines():
    if not line.strip(): continue
    h, rel=line.split('  ',1); p=ROOT/rel
    if not p.is_file(): fail(f'checksum target missing: {rel}'); continue
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=h: fail(f'checksum mismatch: {rel}')
if errors:
    print('PUBLIC RELEASE VALIDATION: FAIL')
    for e in errors: print(' -',e)
    sys.exit(1)
print('PUBLIC RELEASE VALIDATION: PASS')
print(' films=10 scenes=938 features=5 tasks=240 intervals=48')
