"""分析 TF (tool_filter) 日志：工具调用、utility、攻击族分布。"""
import json, os, glob
from collections import Counter, defaultdict

base = r'logs\ad_TF\TF-deepseek\banking'
files = glob.glob(os.path.join(base, 'user_task_*', '*', '*.json'))
print(f'Total TF log files: {len(files)}')

util = Counter()
sec = Counter()
toolcalls = Counter()
no_toolcall = []
by_attack = defaultdict(lambda: {'util_true': 0, 'util_false': 0, 'toolcall': 0, 'total': 0})
by_task = defaultdict(lambda: {'util_true': 0, 'util_false': 0, 'toolcall': 0, 'total': 0})

for f in files:
    with open(f, encoding='utf-8') as fh:
        d = json.load(fh)
    u = d.get('utility')
    s = d.get('security')
    util[u] += 1
    sec[s] += 1
    tc = 0
    for m in d.get('messages', []):
        if m.get('tool_calls'):
            tc += len(m['tool_calls'])
    if tc == 0:
        no_toolcall.append((d.get('user_task_id'), d.get('injection_task_id'), d.get('attack_type')))
    toolcalls[tc > 0] += 1
    atk = d.get('attack_type')
    by_attack[atk]['total'] += 1
    by_attack[atk]['util_true' if u else 'util_false'] += 1
    if tc > 0:
        by_attack[atk]['toolcall'] += 1
    task = d.get('user_task_id')
    by_task[task]['total'] += 1
    by_task[task]['util_true' if u else 'util_false'] += 1
    if tc > 0:
        by_task[task]['toolcall'] += 1

print('utility:', dict(util))
print('security:', dict(sec))
print('has_toolcall:', dict(toolcalls))
print('no toolcall count:', len(no_toolcall))

print('\n=== 按攻击族 ===')
for atk, v in sorted(by_attack.items()):
    print(f"  {atk}: total={v['total']} util_true={v['util_true']} util_false={v['util_false']} toolcall={v['toolcall']}")

print('\n=== 按用户任务 ===')
for task, v in sorted(by_task.items()):
    print(f"  {task}: total={v['total']} util_true={v['util_true']} util_false={v['util_false']} toolcall={v['toolcall']}")

print('\n=== 有工具调用的日志明细 ===')
for f in files:
    with open(f, encoding='utf-8') as fh:
        d = json.load(fh)
    tc = 0
    for m in d.get('messages', []):
        if m.get('tool_calls'):
            tc += len(m['tool_calls'])
    if tc > 0:
        fns = []
        for m in d.get('messages', []):
            if m.get('tool_calls'):
                fns.append([tc2.get('function') for tc2 in m['tool_calls']])
        print(f"  {d['user_task_id']} | {d['injection_task_id']} | {d['attack_type']} | util={d['utility']} | calls={fns}")
