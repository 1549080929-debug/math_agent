"""重新跑预测集的 baseline，完整保存输出（不截断）。

审计修正（2026-08-18）：prediction_experiment.py 把 baseline 输出截断到 800 字符，
导致复盘无法判断 baseline 的真实终局。此脚本补跑并存全量输出，
并用 SymPy 审计后的真答案人工判定。
"""

import json

from baseline import solve_direct

# 真答案来自 audit_standard_answers.py 的 SymPy 审计
TRUE_ANSWERS = {
    1: "a=0 或 a=2",
    2: "x=√5±√3",
    3: "m>1/2",
    4: "x=(3±√5)/2",
    5: "0≤a≤2",
}


def main():
    with open("data/prediction_set.json", encoding="utf-8") as f:
        problems = json.load(f)["problems"]

    results = []
    for p in problems:
        pid = p["id"]
        print(f"[{pid}] 求解中...")
        out = solve_direct(p["question"])
        results.append({
            "id": pid,
            "question": p["question"],
            "predicted_standard_answer": p.get("standard_answer", ""),
            "true_answer": TRUE_ANSWERS.get(pid, ""),
            "baseline_full_output": out,
        })

    with open("data/prediction_baseline_full.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("已保存 data/prediction_baseline_full.json（完整输出，未截断）")


if __name__ == "__main__":
    main()
