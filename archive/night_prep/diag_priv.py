"""Diagnose why priv_D3p group shows ASR=0 (expect 0.717 replication)."""
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

cases = [json.loads(l) for l in open('agentsec/results/night_bounded.jsonl', encoding='utf-8')]
priv = [c for c in cases if c['group'] == 'priv_D3p']

c = priv[0]
print('case:', c['case_id'], '| target:', c['target_tool'])
for r in c['rounds'][:5]:
    print('  R{}: proposal={} | self_auth={} | auth_res={} | invoked={} | state={} | ASR={} | reason={}'.format(
        r['round'], json.dumps(r['model_proposal'], ensure_ascii=False)[:80],
        r['self_authorize_called'], r['authorization_result'], r['tool_invoked'],
        r['state_changed'], r['actionable_success'], r['interception_reason'][:40]))
print('final:', json.dumps(c['final'], ensure_ascii=False)[:250])

sa = sum(1 for c in priv if any(r['self_authorize_called'] for r in c['rounds']))
print('priv 组调用 self_authorize 的 case:', sa, '/ 60')

# tools actually invoked by the model
tools = Counter()
for c in priv:
    for r in c['rounds']:
        tools[r['tool_name']] += 1
print('priv 组模型调用工具分布:', dict(tools))

reasons = Counter()
for c in priv:
    for r in c['rounds']:
        if r['interception_reason']:
            reasons[r['interception_reason'][:50]] += 1
print('priv 组拦截原因:', dict(reasons))
