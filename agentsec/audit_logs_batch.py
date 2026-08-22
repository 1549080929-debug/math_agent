"""自动审计：确认 logs/ad_* 是否包含全部 6 个配置、是否同一批、并从日志文件统计 utility/ASR。

不读取任何已有汇总 json，全部从日志 trace 文件重新统计。
"""
import json
import glob
import os
import datetime
from collections import defaultdict

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
CONFIGS = ['ND', 'N', 'V', 'TF', 'RP', 'SL']  # 论文 §6.5 需要的 6 个配置
EXPECTED_PAIRS = 144  # 6 user tasks x 6 injection tasks x 4 attack families

def find_log_files(cfg):
    """找到 ad_<cfg> 目录下所有 banking 日志 json。"""
    base = os.path.join(LOGS_DIR, f'ad_{cfg}')
    if not os.path.isdir(base):
        return []
    # 结构: ad_<cfg>/<PipelineName>/banking/user_task_*/<attack>/*.json
    files = glob.glob(os.path.join(base, '*', 'banking', 'user_task_*', '*', '*.json'))
    return files

def wilson(k, n, z=1.96):
    """Wilson score interval for a proportion."""
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (center - half, center + half)

import math

print('=' * 80)
print('日志批次完整性审计（全部从 trace 文件统计，不读汇总 json）')
print('=' * 80)

all_ok = True
batch_ranges = {}

for cfg in CONFIGS:
    files = find_log_files(cfg)
    n = len(files)
    if n != EXPECTED_PAIRS:
        all_ok = False
        print(f'\n[!] {cfg}: 文件数 {n} != 期望 {EXPECTED_PAIRS}')
        continue

    # 统计
    util_true = 0
    sec_true = 0
    by_task = defaultdict(lambda: {'u': 0, 's': 0, 'n': 0})
    by_attack = defaultdict(lambda: {'u': 0, 's': 0, 'n': 0})
    mtimes = []
    for f in files:
        try:
            with open(f, encoding='utf-8') as fh:
                d = json.load(fh)
        except Exception as e:
            print(f'[!] {cfg}: 读取失败 {f}: {e}')
            all_ok = False
            continue
        mtimes.append(os.path.getmtime(f))
        if d['utility']:
            util_true += 1
        if d['security']:
            sec_true += 1
        t = d['user_task_id']
        a = d['attack_type']
        by_task[t]['n'] += 1
        by_task[t]['u'] += 1 if d['utility'] else 0
        by_task[t]['s'] += 1 if d['security'] else 0
        by_attack[a]['n'] += 1
        by_attack[a]['u'] += 1 if d['utility'] else 0
        by_attack[a]['s'] += 1 if d['security'] else 0

    tmin = datetime.datetime.fromtimestamp(min(mtimes))
    tmax = datetime.datetime.fromtimestamp(max(mtimes))
    batch_ranges[cfg] = (tmin, tmax)

    # Wilson CI
    asr = sec_true / n
    lo, hi = wilson(sec_true, n)
    util = util_true / n

    print(f'\n=== {cfg} (n={n}) ===')
    print(f'  文件时间: {tmin} ~ {tmax}')
    print(f'  utility = {util_true}/{n} = {util*100:.1f}%')
    print(f'  ASR     = {sec_true}/{n} = {asr*100:.1f}%  Wilson CI [{lo*100:.1f}, {hi*100:.1f}]')
    print('  按任务 (util/sec):', {k: f'{v["u"]}/{v["s"]}/{v["n"]}' for k, v in sorted(by_task.items())})
    print('  按攻击族 (util/sec):', {k: f'{v["u"]}/{v["s"]}/{v["n"]}' for k, v in sorted(by_attack.items())})

print('\n' + '=' * 80)
print('批次一致性检查')
print('=' * 80)
if len(batch_ranges) == 6:
    t0 = min(v[0] for v in batch_ranges.values())
    t1 = max(v[1] for v in batch_ranges.values())
    span = (t1 - t0).total_seconds() / 60
    print(f'  6 个配置日志时间跨度: {t0} ~ {t1}（{span:.0f} 分钟）')
    # 按开始时间排序，检查配置间是否有大间隙（>30 分钟视为不同批次）
    ordered = sorted(batch_ranges.items(), key=lambda kv: kv[1][0])
    prev_end = None
    gaps = []
    for cfg, (tmin, tmax) in ordered:
        if prev_end is not None:
            gap = (tmin - prev_end).total_seconds() / 60
            gaps.append((cfg, gap))
        prev_end = tmax
    max_gap = max(g for _, g in gaps) if gaps else 0
    for cfg, g in gaps:
        flag = ' [!]' if g > 30 else ''
        print(f'  {cfg} 与上一配置间隔: {g:.1f} 分钟{flag}')
        if g > 30:
            all_ok = False
    print(f'  最大间隔: {max_gap:.1f} 分钟（<30 分钟 = 连续同一批）')
    print(f'  配置顺序: {" -> ".join(c for c, _ in ordered)}')
else:
    all_ok = False
    print(f'  [!] 只找到 {len(batch_ranges)}/6 个配置的日志')

if all_ok:
    print('\n结论: [OK] 6 配置齐全、时间连续（同一批）、全部 864 条 trace 可追溯')
else:
    print('\n结论: [FAIL] 存在问题，见上方 [!]')
