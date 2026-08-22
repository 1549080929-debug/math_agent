"""验证 trace 完整性：每个用例是否有完整记录。"""
import json
import glob
import os

files = sorted(glob.glob('traces/*.json'))
print(f'trace 文件数: {len(files)}')

for f in ['traces/ND_direct_M0.json', 'traces/N_direct_M6.json', 'traces/V_direct_M0.json', 'traces/ND_benign.json', 'traces/V_indirect_M3.json']:
    if not os.path.exists(f):
        print(f'  [缺] {f}')
        continue
    d = json.load(open(f, encoding='utf-8'))
    print(f'  {os.path.basename(f)}:')
    print(f'    keys={list(d.keys())}')
    print(f'    mcp_tool_description[:70]={d.get("mcp_tool_description", "")[:70]}')
    print(f'    rounds={len(d.get("rounds", []))}, final={d.get("final")}')
    for r in d.get('rounds', [])[:2]:
        raw = (r.get('llm_raw_output') or '')[:70]
        print(f'    round{r.get("round")}: llm_raw={raw!r}')
        print(f'      proposal={r.get("proposal")}, decision={r.get("decision")}')
        if 'defense' in r:
            print(f'      defense={r["defense"]}')
    print()

# 汇总统计：验证 ASR 数字可追溯
print('=== 汇总验证（从 trace 重新统计） ===')
from collections import defaultdict
by_cfg = defaultdict(list)
for f in files:
    name = os.path.basename(f)
    if 'benign' in name:
        continue
    cfg = name.split('_')[0]
    d = json.load(open(f, encoding='utf-8'))
    by_cfg[cfg].append(d['final']['executed_high_risk'])

for cfg in ['ND', 'N', 'V']:
    lst = by_cfg.get(cfg, [])
    if lst:
        print(f'  {cfg}: {sum(lst)}/{len(lst)} 高风险执行 = {sum(lst)/len(lst):.3f}')
