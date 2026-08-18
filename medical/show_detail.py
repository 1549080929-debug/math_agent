import json

data = json.load(open("medical/data_baseline_hard.json", encoding="utf-8"))
for d in data:
    if d["id"] in (103, 104):
        c, o = d["case"], d["llm_output"]
        print(f"=== #{c['id']} {c['chief_complaint']} | lab: {c['lab']}")
        print(f"  最可能: {o.get('most_likely_diagnosis')} | conf={o.get('confidence')}")
        print(f"  建议检查: {o.get('additional_workup', [])}")
        print()
