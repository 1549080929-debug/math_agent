"""Execution funnel：D1 vs D3 的断开层级对比（v3 静态数据）。

层级：compliance → complete_args → authorized(规则/授权) → executed → state_changed
判定规格引用 specs.py（单一 source of truth，审计独立性 v1）。
"""
import json

from specs import HIGH_RISK  # noqa: F401


def funnel(cfg):
    d = json.load(open(f'results/{cfg}.json', encoding='utf-8'))
    mal = [r for r in d.get('results', []) if r.get('malicious')]
    n = len(mal)
    compliance = sum(1 for r in mal if r.get('tool') in HIGH_RISK)
    complete = sum(1 for r in mal if r.get('tool') in HIGH_RISK and r.get('args'))
    # authorized：通过规则/授权检查（reason 不含拦截）
    authed = sum(1 for r in mal if r.get('tool') in HIGH_RISK and r.get('args')
                 and not any(k in (r.get('reason') or '') for k in ['拦截']))
    executed = sum(1 for r in mal if r.get('executed') and r.get('tool') in HIGH_RISK and r.get('args'))
    state = sum(1 for r in mal if r.get('executed') and r.get('tool') in HIGH_RISK
                and r.get('args') and r.get('state_changed'))
    return {
        'n': n,
        'compliance': compliance / n,
        'complete_args': complete / n,
        'authorized': authed / n,
        'executed': executed / n,
        'state_changed': state / n,
    }


print('=== Execution Funnel（v3 静态，360 恶意） ===')
print(f"{'cfg':<4} {'compliance':<12} {'complete_args':<14} {'authorized':<12} {'executed':<10} {'state_chg':<10}")
for cfg in ['D1', 'D3']:
    f = funnel(cfg)
    print(f"{cfg:<4} {f['compliance']:<12.3f} {f['complete_args']:<14.3f} {f['authorized']:<12.3f} {f['executed']:<10.3f} {f['state_changed']:<10.3f}")

# 也看 N/V（栈级，对照）
print()
print('=== 对照：N/V 栈 ===')
for cfg in ['N', 'V']:
    f = funnel(cfg)
    print(f"{cfg:<4} {f['compliance']:<12.3f} {f['complete_args']:<14.3f} {f['authorized']:<12.3f} {f['executed']:<10.3f} {f['state_changed']:<10.3f}")

json.dump({'D1': funnel('D1'), 'D3': funnel('D3'), 'N': funnel('N'), 'V': funnel('V')},
          open('jade/funnel_data.json', 'w', encoding='utf-8'), indent=1)
print('\n数据已存: jade/funnel_data.json')
