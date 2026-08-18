"""显示预测集 baseline 完整输出的结尾（最终答案区域）。"""

import json

with open("data/prediction_baseline_full.json", encoding="utf-8") as f:
    results = json.load(f)

for r in results:
    out = r["baseline_full_output"].strip()
    tail = out[-300:].replace("\n", " ")
    print(f"=== 题 {r['id']} | 真答案: {r['true_answer']} | 预测表标准答案: {r['predicted_standard_answer']}")
    print(f"  结尾: ...{tail}")
    print()
