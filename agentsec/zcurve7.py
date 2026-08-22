"""7 轮 Z(α) 数据提取。"""
import json
import os

files = {
    'D1': 'results/adaptivekimi_D1.json',
    'D2': 'results/adaptivekimi_D2.json',
    'D3': 'results/adaptivekimi_D3.json',
    'D4': 'results/adaptivekimi_D4.json',
}
static = {'D1': 0.000, 'D2': 0.200, 'D3': 0.000, 'D4': 0.067}

print('=== 7 轮每轮累计 ASR ===')
all_z = {}
for cfg in ['D1', 'D2', 'D3', 'D4']:
    f = files[cfg]
    d = json.load(open(f, encoding='utf-8'))
    rows = d.get('rows', [])
    rounds = d.get('rounds', 7)
    n = len(rows)
    per_round = [0] * (rounds + 1)
    for r in rows:
        if r.get('success'):
            ru = r.get('rounds', rounds)
            if ru is None or ru > rounds:
                ru = rounds
            per_round[ru] += 1
    cum = []
    acc = 0
    for r in range(1, rounds + 1):
        acc += per_round[r]
        cum.append(acc / n)
    all_z[cfg] = {'static': static[cfg], 'cum': cum, 'n': n, 'rounds': rounds,
                  'asr': d.get('asr'), 'comply': d.get('comply_rate')}
    print(f'  {cfg}: n={n} rounds={rounds} 静态={static[cfg]:.3f} 最终ASR={d.get("asr"):.3f} 合规={d.get("comply_rate"):.3f}')
    print(f'    每轮累计: {[round(c,3) for c in cum]}')

print()
print('=== Z(α) 矩阵（静态 + 轮1-7） ===')
print(f"{'cfg':<4} " + ' '.join(f'α{i}' for i in range(8)))
for cfg in ['D1', 'D2', 'D3', 'D4']:
    z = all_z.get(cfg)
    if not z:
        continue
    pts = [z['static']] + z['cum']
    print(f"{cfg:<4} " + ' '.join(f'{p:.3f}' for p in pts))

# 存数据供画图
json.dump(all_z, open('jade/zcurve7_data.json', 'w', encoding='utf-8'), indent=1)
print('\n数据已存: jade/zcurve7_data.json')
