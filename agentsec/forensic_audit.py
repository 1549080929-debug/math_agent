"""小型 forensic audit：检查 7 轮 adaptive 结果无 stale/duplicate，抽样核对。

检查项：
1. 每个文件：rows=30、无重复 scenario、声明 rounds=7、success 的 rounds 合法（≤7）
2. D1/D3 抽样：5 compliance + 5 non-compliance（核对 comply 与 target）
3. D2/D4 抽样：每轮突破分布 + 随机 5 条
"""
import json
import random
from collections import Counter

random.seed(42)

files = {
    'D1': 'results/adaptivekimi_D1.json',
    'D2': 'results/adaptivekimi_D2.json',
    'D3': 'results/adaptivekimi_D3.json',
    'D4': 'results/adaptivekimi_D4.json',
}

print('=' * 70)
print('FORENSIC AUDIT: 7-round adaptive results')
print('=' * 70)

for cfg, f in files.items():
    d = json.load(open(f, encoding='utf-8'))
    rows = d.get('rows', [])
    declared = d.get('rounds')
    scenarios = [r['scenario'] for r in rows]
    dup = [s for s, c in Counter(scenarios).items() if c > 1]
    # success 的 rounds 合法性
    bad_rounds = [r['scenario'] for r in rows if r.get('success') and (r.get('rounds') is None or r.get('rounds') > declared)]
    # 每轮突破分布
    per_round = Counter(r.get('rounds') for r in rows if r.get('success'))
    print(f'\n[{cfg}] 声明rounds={declared} rows={len(rows)}')
    print(f'  重复scenario: {dup if dup else "无"}')
    print(f'  非法rounds: {bad_rounds if bad_rounds else "无"}')
    print(f'  每轮突破分布: {dict(sorted(per_round.items()))}')
    print(f'  ASR={d.get("asr"):.3f} 合规={d.get("comply_rate"):.3f}')

# 抽样：D1/D3 各 10 条（5 compliance + 5 non）
print('\n' + '=' * 70)
print('抽样核对: D1/D3 (5 compliance + 5 non-compliance)')
print('=' * 70)
for cfg in ['D1', 'D3']:
    d = json.load(open(files[cfg], encoding='utf-8'))
    rows = d.get('rows', [])
    comp = [r for r in rows if r.get('comply')]
    non = [r for r in rows if not r.get('comply')]
    print(f'\n[{cfg}] comply={len(comp)} non={len(non)}')
    print('  compliance 抽样:')
    for r in random.sample(comp, min(5, len(comp))):
        print(f"    {r['scenario']}: success={r['success']} rounds={r['rounds']} target={r['target']}")
    print('  non-compliance 抽样:')
    for r in random.sample(non, min(5, len(non))):
        print(f"    {r['scenario']}: success={r['success']} rounds={r['rounds']} target={r['target']}")

# 抽样：D2/D4 随机 5 条
print('\n' + '=' * 70)
print('抽样核对: D2/D4 随机 5 条')
print('=' * 70)
for cfg in ['D2', 'D4']:
    d = json.load(open(files[cfg], encoding='utf-8'))
    rows = d.get('rows', [])
    print(f'\n[{cfg}]')
    for r in random.sample(rows, 5):
        print(f"    {r['scenario']}: success={r['success']} rounds={r['rounds']} comply={r['comply']} target={r['target']}")
