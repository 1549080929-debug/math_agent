"""打印 20 题测试集的系统 vs baseline 对比（baseline 显示结尾终局答案）。"""

import json

# 系统的判定（人工阅读 testset_results.json 后给出）
SYSTEM_JUDGE = {
    1: "OK", 2: "OK", 3: "OK", 4: "系统未解决", 5: "OK(未验证)", 6: "OK", 7: "OK",
    8: "OK(未验证)", 9: "系统未解决", 10: "OK", 11: "OK(未验证)", 12: "OK(未验证)",
    13: "OK(未验证)", 14: "OK", 15: "OK(未验证)", 16: "错(给了[1,∞))", 17: "OK(未验证)",
    18: "错(给了a≥4)", 19: "OK(未验证)", 20: "OK(未验证)",
}

with open("data/testset_results.json", encoding="utf-8") as f:
    sys_results = {r["id"]: r for r in json.load(f)}
with open("data/testset_baseline.json", encoding="utf-8") as f:
    base_results = {r["id"]: r for r in json.load(f)}

print(f"{'#':>2} {'L':>2} {'系统':<16} {'sys验证':<12} baseline 终局")
print("-" * 100)
for pid in range(1, 21):
    s = sys_results[pid]
    b = base_results[pid]
    base_tail = b["answer"].strip().replace("\n", " ")[-160:]
    sc = s.get("status_counts", {})
    v = f"P{sc.get('PASS',0)}/U{sc.get('UNSURE',0)}" if sc else "—"
    print(f"{pid:>2} {s['level']:>2} {SYSTEM_JUDGE[pid]:<16} {v:<12} ...{base_tail}")
