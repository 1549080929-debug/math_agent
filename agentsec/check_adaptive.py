"""检查自适应/白盒数据。"""
import json

for f in ['adaptive_D2.json', 'adaptive_D4.json', 'adaptive_N.json', 'adaptive_V.json',
          'adaptivewb_N.json', 'adaptivewb_V.json', 'adaptivewb_ds_N.json', 'adaptivewb_ds_V.json']:
    try:
        d = json.load(open('results/' + f, encoding='utf-8'))
        print(f"{f}: asr={d.get('asr')} comply={d.get('comply_rate')} n={d.get('scenario_count')} rounds={d.get('rounds')} whitebox={d.get('whitebox')}")
    except Exception as e:
        print(f'{f}: ERR {e}')

# 良性（v3）
print()
for name in ['D1', 'D2', 'D3', 'D4']:
    try:
        d = json.load(open(f'results/{name}_benign.json', encoding='utf-8'))
        results = d.get('results', [])
        ok = sum(1 for r in results if r.get('executed') and r.get('tool') == r.get('target_tool') and r.get('args'))
        print(f'{name}_benign: {ok}/{len(results)} = {ok/len(results) if results else 0:.3f}')
    except Exception as e:
        print(f'{name}_benign: ERR {e}')
