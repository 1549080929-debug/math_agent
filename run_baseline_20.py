"""跑 20 题测试集的 baseline（直接求解，全量输出），增量保存。"""

import json

from baseline import solve_direct


def main():
    with open("data/problems_20.json", encoding="utf-8") as f:
        problems = json.load(f)

    try:
        with open("data/testset_baseline.json", encoding="utf-8") as f:
            results = json.load(f)
        done_ids = {r["id"] for r in results}
    except Exception:
        results, done_ids = [], set()

    for p in problems:
        if p["id"] in done_ids:
            print(f"[{p['id']}/20] L{p['level']} 已跑过，跳过")
            continue
        print(f"[{p['id']}/20] L{p['level']} baseline 求解中...")
        try:
            out = solve_direct(p["question"])
            results.append({
                "id": p["id"], "level": p["level"], "question": p["question"],
                "standard_answer": p.get("standard_answer", ""),
                "answer": out,
            })
        except Exception as e:
            results.append({"id": p["id"], "level": p["level"], "question": p["question"],
                            "answer": f"[异常] {e}"})
        with open("data/testset_baseline.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n完成：{len(results)}/20，已保存 data/testset_baseline.json")


if __name__ == "__main__":
    main()
