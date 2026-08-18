"""基线对比：不走拆解-验证流程，直接让 DeepSeek 解题（单次输出）。

用于对照实验：证明"拆解→验证→纠错→组合"架构的价值。
"""

import json

from llm_client import chat


def solve_direct(question):
    sys = "你是数学解题助手。请一步一步思考并求解下面的题，最后单独一行给出'最终答案：...'。"
    text = chat([
        {"role": "system", "content": sys},
        {"role": "user", "content": question},
    ], temperature=0.2, max_tokens=1500)
    return text


def main():
    with open("data/problems.json", encoding="utf-8") as f:
        problems = json.load(f)

    results = []
    for i, p in enumerate(problems, 1):
        print(f"[{i}/{len(problems)}] 直接求解：{p['question'][:40]}...")
        answer = solve_direct(p["question"])
        results.append({
            "question": p["question"],
            "standard_answer": p.get("standard_answer", ""),
            "raw_output": answer,
        })

    with open("data/baseline_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n已保存 data/baseline_results.json")


if __name__ == "__main__":
    main()
