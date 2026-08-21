"""分攻击族报告 ND ASR，确认每个攻击族都生效。"""
import json, glob, os
from collections import defaultdict

base = r'logs\ad_ND\ND-deepseek\banking'
files = glob.glob(os.path.join(base, 'user_task_*', '*', '*.json'))
print(f'ND total files: {len(files)}')

by_attack = defaultdict(lambda: {'sec_true': 0, 'sec_false': 0, 'util_true': 0, 'util_false': 0, 'total': 0})
for f in files:
    with open(f, encoding='utf-8') as fh:
        d = json.load(fh)
    atk = d['attack_type']
    by_attack[atk]['total'] += 1
    by_attack[atk]['sec_true' if d['security'] else 'sec_false'] += 1
    by_attack[atk]['util_true' if d['utility'] else 'util_false'] += 1

print('\n=== ND 分攻击族 ===')
for atk in ['direct', 'ignore_previous', 'injecagent', 'system_message']:
    v = by_attack[atk]
    asr = v['sec_true'] / v['total'] if v['total'] else 0
    util = v['util_true'] / v['total'] if v['total'] else 0
    print(f'  {atk}: n={v["total"]} ASR={asr:.3f} ({v["sec_true"]}/{v["total"]}) utility={util:.3f} ({v["util_true"]}/{v["total"]})')

# 也看每个攻击族下哪些 user_task 被攻破
print('\n=== ND 分攻击族 × 用户任务 (ASR=1 的) ===')
for atk in ['direct', 'ignore_previous', 'injecagent', 'system_message']:
    hits = []
    for f in files:
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        if d['attack_type'] == atk and d['security']:
            hits.append((d['user_task_id'], d['injection_task_id']))
    print(f'  {atk}: {len(hits)} 攻击成功 -> {hits}')
