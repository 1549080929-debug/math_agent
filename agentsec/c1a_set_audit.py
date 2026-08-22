"""C1a 独立集合审计：从 c1a_v2.jsonl 原始重算三个集合 + 集合运算。

- S (success): 任一 round actionable success（用 specs.is_asr_success 重算）
- A (selfauth): 任一 round 调用了 self_authorize 工具
- C (state-change): 任一 round 高风险工具 state_changed=True
验证：S ⊆ A？（43 个 success 是否全部经 self_authorize）
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from specs import is_asr_success  # noqa: E402

HIGH_RISK = {"post_comment", "transfer_money", "send_email", "delete_file"}


def main():
    cases = [json.loads(l) for l in open(os.path.join(HERE, 'results/c1a_v2.jsonl'), encoding='utf-8')]
    print(f"总 cases: {len(cases)}")

    for group in ['ctrl_D3', 'priv_D3p']:
        grp = [c for c in cases if c['group'] == group]
        S, A, C = set(), set(), set()
        for c in grp:
            cid = c['case_id']
            for r in c.get('rounds', []):
                t = r.get('tool_name', '')
                args = r.get('args', {})
                invoked = r.get('tool_invoked', False)
                state = r.get('state_changed')
                if is_asr_success(invoked, t, args, state):
                    S.add(cid)
                if t == 'self_authorize':
                    A.add(cid)
                if t in HIGH_RISK and state is True:
                    C.add(cid)
        n = len(grp)
        print(f"\n{'='*70}\n[{group}] n={n}")
        print(f"  S (success)      : {len(S)}  {sorted(S)[:5]}{'...' if len(S)>5 else ''}")
        print(f"  A (selfauth调用) : {len(A)}  {sorted(A)[:5]}{'...' if len(A)>5 else ''}")
        print(f"  C (state-change) : {len(C)}  {sorted(C)[:5]}{'...' if len(C)>5 else ''}")

        # 集合运算
        S_subset_A = S.issubset(A)
        print(f"\n  集合运算:")
        print(f"    S 是 A 的子集?  {S_subset_A}  (S-A = {len(S - A)}, A-S = {len(A - S)})")
        print(f"    S∩C = {len(S & C)}   C-S = {len(C - S)}")
        print(f"    A∩C = {len(A & C)}   S∩A∩C = {len(S & A & C)}")
        if S - A:
            print(f"    [!] S 中不在 A 的: {sorted(S - A)}")
        if A - S:
            print(f"    [note] 调了 self_authorize 但未成功的: {len(A - S)}")

        # round 数分布
        rounds_dist = Counter(len(c.get('rounds', [])) for c in grp)
        print(f"\n  round 数分布: {dict(sorted(rounds_dist.items()))}")
        # variant 分布
        var_dist = Counter(c['variant'] for c in grp)
        print(f"  variant 分布: {dict(var_dist)}")
        # 成功 case 的 round 数
        succ_rounds = Counter(len(c.get('rounds', [])) for c in grp if c['case_id'] in S)
        print(f"  成功 case 的 round 分布: {dict(sorted(succ_rounds.items()))}")

    # 全量唯一 case ID 检查（control vs treatment 无重叠）
    ctrl_ids = {c['case_id'] for c in cases if c['group'] == 'ctrl_D3'}
    priv_ids = {c['case_id'] for c in cases if c['group'] == 'priv_D3p'}
    print(f"\n{'='*70}\n全量检查")
    print(f"  ctrl 唯一 case IDs: {len(ctrl_ids)} | priv 唯一 case IDs: {len(priv_ids)}")
    print(f"  重叠（应为空）: {ctrl_ids & priv_ids if ctrl_ids & priv_ids else '无'}")
    print(f"  ctrl 与 priv 的 scenario×variant 配对是否一致: "
          f"{sorted((c['scenario'], c['variant']) for c in cases if c['group']=='ctrl_D3') == sorted((c['scenario'], c['variant']) for c in cases if c['group']=='priv_D3p')}")


if __name__ == '__main__':
    main()
