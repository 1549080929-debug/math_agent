"""Diagnose why bounded_D3p group shows ASR=0.717 (expect suppression)."""
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

cases = [json.loads(l) for l in open('agentsec/results/night_bounded.jsonl', encoding='utf-8')]
bounded = [c for c in cases if c['group'] == 'bounded_D3p']

# 1) full trace of first successful bounded case
succ_cases = [c for c in bounded if c['final'].get('success') or c['final'].get('actionable_success')]
print('bounded success cases:', len(succ_cases), '/ 60')
if succ_cases:
    c = succ_cases[0]
    print('case:', c['case_id'])
    for r in c['rounds']:
        print('  R{}: tool={} self_auth={} auth_res={} invoked={} state={} ASR={}'.format(
            r['round'], r['tool_name'], r['self_authorize_called'], r['authorization_result'],
            r['tool_invoked'], r['state_changed'], r['actionable_success']))
    print('final:', json.dumps(c['final'], ensure_ascii=False))

# 2) authorization_result values across all bounded rounds
auth = Counter()
for c in bounded:
    for r in c['rounds']:
        auth[str(r['authorization_result'])[:60]] += 1
print('bounded 组 authorization_result 分布:', dict(auth))

# 3) any sign of TTL/single-use in trace (撤销/过期/重复授权)?
revoked = 0
multi_sa = 0
for c in bounded:
    sa_rounds = [r['round'] for r in c['rounds'] if r['self_authorize_called']]
    if len(sa_rounds) > 1:
        multi_sa += 1
print('bounded 组多次调用 self_authorize 的 case:', multi_sa, '/ 60')
