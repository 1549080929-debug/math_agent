"""Inspect adaptive output json real structure."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
for name in ['D1', 'D3']:
    p = f'agentsec/results/adaptivekimi_night2_{name}.json'
    d = json.load(open(p, encoding='utf-8'))
    print(f'--- {name}: type={type(d).__name__}')
    if isinstance(d, dict):
        for k, v in d.items():
            sz = len(v) if hasattr(v, '__len__') else ''
            print(f'  key={k!r} type={type(v).__name__} len={sz}')
            if isinstance(v, list) and v:
                print('    first elem keys:', list(v[0].keys()) if isinstance(v[0], dict) else v[0])
                print('    first elem:', json.dumps(v[0], ensure_ascii=False)[:400])
                break
    elif isinstance(d, list):
        print('  list len:', len(d))
        if d:
            print('  first:', json.dumps(d[0], ensure_ascii=False)[:400])
