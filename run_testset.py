"""跑 20 题测试集（系统：拆解-验证-纠错），增量保存结果。"""

import json

from main import run_problem


def main():
    with open("data/problems_20.json", encoding="utf-8") as f:
        problems = json.load(f)

    try:
        with open("data/testset_results.json", encoding="utf-8") as f:
            results = json.load(f)
        done_ids = {r["id"] for r in results}
    except Exception:
        results, done_ids = [], set()

    for p in problems:
        if p["id"] in done_ids:
            print(f"[{p['id']}/20] L{p['level']} 已跑过，跳过")
            continue
        print(f"[{p['id']}/20] L{p['level']} 系统求解中...")
        try:
            r = run_problem(p["question"], standard_answer=p.get("standard_answer"), verbose=False)
            results.append({
                "id": p["id"], "level": p["level"], "question": p["question"],
                "standard_answer": p.get("standard_answer", ""),
                "ok": bool(r.get("ok")),
                "all_subtasks_verified": bool(r.get("all_subtasks_verified")),
                "has_final_check": bool(r.get("has_final_check")),
                "final_verify": r.get("final_verify", "UNSURE"),
                "answer_verified": bool(r.get("answer_verified")),
                "final_answer": r.get("final_answer", ""),
                "status_counts": r.get("status_counts", {}),
                "answer": (r.get("answer") or "")[:2000] if r.get("ok") else "[系统未解决]",
            })
        except Exception as e:
            results.append({"id": p["id"], "level": p["level"], "question": p["question"],
                            "ok": False, "answer": f"[异常] {e}", "status_counts": {}})
        with open("data/testset_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n完成：{len(results)}/20，已保存 data/testset_results.json")


if __name__ == "__main__":
    main()
