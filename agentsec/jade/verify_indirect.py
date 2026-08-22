"""验证 ND 下 indirect 投毒的真实成功率。"""
import json
import glob
import os

files = sorted(glob.glob('traces/ND_indirect_*.json'))
files = [f for f in files if 'benign' not in f]
print(f'ND indirect 用例数: {len(files)}')
succ = 0
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    ok = d['final']['executed_high_risk']
    succ += 1 if ok else 0
    print(f"  {os.path.basename(f)}: executed={ok} tool={d['final']['tool']}")
print(f'合计: {succ}/{len(files)} 成功 = {succ/len(files):.3f}')
