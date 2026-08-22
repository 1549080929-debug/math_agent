"""检查结果文件的真实 rounds。"""
import json

for f in ['results/adaptivekimi_D1.json', 'results/adaptive_D2.json',
          'results/adaptivekimi_D3.json', 'results/adaptive_D4.json']:
    d = json.load(open(f, encoding='utf-8'))
    rows = d.get('rows', [])
    max_r = max((r.get('rounds', 0) for r in rows if r.get('success')), default=0)
    succ = sum(1 for r in rows if r.get('success'))
    print(f"{f}: 声明rounds={d.get('rounds')} rows={len(rows)} ASR={d.get('asr')} 成功={succ} 最大突破轮次={max_r}")
