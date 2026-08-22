"""检查 D1.json 中 send_email 空参数记录的 state_changed。"""
import json
from collections import Counter

d = json.load(open('results/D1.json', encoding='utf-8'))
print('D1 version:', d.get('scenario_version'), 'dry:', d.get('dry_run'))
mal = [r for r in d.get('results', []) if r.get('malicious')]
print(f'恶意: {len(mal)}')

# send_email 记录明细
se = [r for r in mal if r.get('tool') == 'send_email']
print(f'send_email 记录: {len(se)}')
state_ct = Counter((r.get('executed'), bool(r.get('args')), r.get('state_changed')) for r in se)
for k, v in state_ct.most_common(6):
    print(f'  (executed={k[0]}, args非空={k[1]}, state_changed={k[2]}): {v}')
print('样例:')
for r in se[:4]:
    print(f'  args={r.get("args")} executed={r.get("executed")} state={r.get("state_changed")} reason={r.get("reason","")[:50]}')
