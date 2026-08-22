"""检查 D2.json 的实际记录分布。"""
import json

d = json.load(open('results/D2.json', encoding='utf-8'))
print('config:', d.get('config'), '| version:', d.get('scenario_version'), '| dry:', d.get('dry_run'))
results = d.get('results', [])
mal = [r for r in results if r.get('malicious')]
print(f'总 {len(results)} 例, 恶意 {len(mal)} 例')

from collections import Counter
executed = Counter()
tools = Counter()
state = Counter()
for r in mal:
    executed[r.get('executed')] += 1
    tools[r.get('tool')] += 1
    state[(r.get('executed'), bool(r.get('args')), r.get('state_changed'))] += 1

print('executed 分布:', dict(executed))
print('tool 分布:', dict(tools))
print('(executed, args非空, state_changed) 分布:')
for k, v in state.most_common(10):
    print(f'  {k}: {v}')

# 看几个 executed=True 的样例
print()
print('=== executed=True 样例 ===')
n = 0
for r in mal:
    if r.get('executed'):
        print(f'  tool={r["tool"]} args={r["args"]} state={r.get("state_changed")} reason={r.get("reason","")[:40]}')
        n += 1
        if n >= 5:
            break
