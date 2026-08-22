"""检查 adaptivekimi_* 文件的真实 rounds。"""
import json
import glob
import os

for f in sorted(glob.glob('results/adaptivekimi_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    rows = d.get('rows', [])
    succ = sum(1 for r in rows if r.get('success'))
    max_r = max((r.get('rounds', 0) for r in rows if r.get('success')), default=0)
    print(f"{os.path.basename(f)}: rounds={d.get('rounds')} rows={len(rows)} ASR={d.get('asr')} 成功={succ} 最大突破轮次={max_r}")
