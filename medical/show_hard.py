import json

data = json.load(open("medical/data_baseline_hard.json", encoding="utf-8"))
for d in data:
    c, o = d["case"], d["llm_output"]
    print(f"#{c['id']} [{c['category']}] 确诊: {c['confirmed_diagnosis']}")
    print(f"  LLM: {o.get('most_likely_diagnosis', '?')} | conf={o.get('confidence')} | urgent={o.get('urgent_action_needed')}")
    print(f"  鉴别: {o.get('differential_diagnosis', [])[:3]}")
    print()
