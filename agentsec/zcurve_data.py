"""从已有 adaptive 结果提取每轮累计 ASR（Z(α) 曲线数据）。"""
import json
import os

# 静态 ASR（v3 重跑后）
static = {'D1': 0.000, 'D2': 0.200, 'D3': 0.000, 'D4': 0.067}

# 自适应文件：D1/D3 是 adaptivekimi_*（黑盒自适应跑出的文件名带 kimi suffix）
files = {
    'D1': 'results/adaptivekimi_D1.json',
    'D2': 'results/adaptive_D2.json',
    'D3': 'results/adaptivekimi_D3.json',
    'D4': 'results/adaptive_D4.json',
}

print('=== 每轮累计 ASR（Z(α) 数据） ===')
zdata = {}
for cfg in ['D1', 'D2', 'D3', 'D4']:
    f = files[cfg]
    if not os.path.exists(f):
        print(f'  [缺] {cfg}: {f}')
        continue
    d = json.load(open(f, encoding='utf-8'))
    rows = d.get('rows', [])
    rounds = d.get('rounds', 3)
    n = len(rows)
    # rounds_used 分布：success=True 的 row 的 rounds = 突破轮次
    per_round = [0] * (rounds + 1)  # per_round[r] = 恰好第 r 轮突破数
    for r in rows:
        if r.get('success'):
            ru = r.get('rounds', rounds)
            if ru is None or ru > rounds:
                ru = rounds
            per_round[ru] += 1
    # 累计：ASR(α=r) = 前 r 轮内突破比例
    cum = []
    acc = 0
    for r in range(1, rounds + 1):
        acc += per_round[r]
        cum.append(acc / n)
    zdata[cfg] = {'static': static[cfg], 'per_round': per_round, 'cum': cum, 'n': n, 'rounds': rounds}
    print(f'  {cfg}: n={n} rounds={rounds} 静态={static[cfg]:.3f} 每轮突破={per_round[1:]} 累计={[round(c,3) for c in cum]}')

print()
print('=== Z(α) 矩阵（α = 静态/轮1/轮2/轮3） ===')
print(f"{'cfg':<4} {'α=静态':<8} {'α=轮1':<8} {'α=轮2':<8} {'α=轮3':<8}")
for cfg in ['D1', 'D2', 'D3', 'D4']:
    z = zdata.get(cfg)
    if not z:
        continue
    pts = [z['static']] + z['cum']
    print(f"{cfg:<4} " + " ".join(f"{p:<8.3f}" for p in pts))
