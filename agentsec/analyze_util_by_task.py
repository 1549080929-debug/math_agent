"""按用户任务统计各配置的 utility。"""
import json, glob, os
from collections import defaultdict

for cfg in ['ad_V', 'ad_ND', 'ad_N', 'ad_TF', 'ad_RP', 'ad_SL']:
    base = os.path.join(r'logs', cfg, f'{cfg.replace("ad_","").upper()}-deepseek', 'banking')
    if not os.path.isdir(base):
        # 尝试其他命名
        base = os.path.join(r'logs', cfg)
        if not os.path.isdir(base):
            print(f'{cfg}: no logs dir')
            continue
    files = glob.glob(os.path.join(base, 'user_task_*', '*', '*.json'))
    by_task = defaultdict(lambda: {'true': 0, 'false': 0, 'total': 0})
    for f in files:
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        t = d['user_task_id']
        by_task[t]['total'] += 1
        by_task[t]['true' if d['utility'] else 'false'] += 1
    print(f'=== {cfg} (n={len(files)}) ===')
    for t in sorted(by_task):
        v = by_task[t]
        print(f'  {t}: util_true={v["true"]} util_false={v["false"]} total={v["total"]}')
    print()
