"""展示一个 priv 成功 case 的完整 trace。"""
import json

cases = [json.loads(l) for l in open('results/c1a_v2.jsonl', encoding='utf-8')]
priv_succ = [c for c in cases if c['group'] == 'priv_D3p' and c['final']['success']]
print(f'priv 成功 case 数: {len(priv_succ)}')

for c in priv_succ[:3]:
    print(f"\n=== {c['case_id']} target={c['target_tool']} ===")
    for r in c['rounds']:
        print(f"  轮{r['round']}: tool={r['tool_name']} args={r['args']}")
        print(f"    self_auth_called={r['self_authorize_called']} auth_result={str(r['authorization_result'])[:45]}")
        print(f"    invoked={r['tool_invoked']} state={r['state_changed']} actionable={r['actionable_success']}")
