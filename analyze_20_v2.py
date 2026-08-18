"""分析带防御重跑后的 20 题结果：正确性判定 + 终局验证统计。"""

import json

with open("data/testset_results.json", encoding="utf-8") as f:
    results = {r["id"]: r for r in json.load(f)}

print(f"{'#':>2} {'L':>2} {'终局验证':<8} {'verified':<9} {'最终答案(结构化)':<24} 判定")
print("-" * 100)
ok_cnt = 0
for pid in range(1, 21):
    r = results[pid]
    std = r["standard_answer"]
    fa = r.get("final_answer", "")
    fv = r.get("final_verify", "-")
    av = "✅" if r.get("answer_verified") else "—"
    # 判定：先看有没有 final_answer，再看是否与标准答案一致（人工判断）
    judge = "待判"
    ok_cnt += 0
    print(f"{pid:>2} {r['level']:>2} {fv:<8} {av:<9} {fa[:22]:<24} | 标准:{std}")
