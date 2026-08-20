"""PPMF 式自审计：终局验证规格回退路径的诚实度对比（修前 vs 修后）。

修前 = data/testset_results.json（历史运行）；修后 = 应用 main.py 第 4 波降级后的确定性变换
（fc_source=="llm" 且终局验证 PASS → UNSURE，PPMF 式 fail-closed）。

用法：python reliability/audit_fallback.py
"""
import json
import io
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from final_check_deriver import derive_final_check  # noqa: E402


def main():
    with io.open(os.path.join(ROOT, "data", "testset_results.json"), encoding="utf-8") as f:
        results = json.load(f)

    rows = []
    for it in results:
        rule_fc, reason = derive_final_check(it["question"])
        # 重建 fc_source（与 main.py 决策一致：规则派生 > LLM 声明 > 无）
        if rule_fc:
            fc_source = "rule"
        elif it.get("has_final_check"):
            fc_source = "llm"
        else:
            fc_source = "none"
        before = it["final_verify"]
        # 修后：llm 规格 + PASS → UNSURE（PPMF 式 fail-closed）
        after = "UNSURE" if (fc_source == "llm" and before == "PASS") else before
        rows.append({"id": it["id"], "fc_source": fc_source,
                     "before": before, "after": after,
                     "before_verified": it.get("answer_verified"),
                     "after_verified": after == "PASS"})

    print("== 终局验证规格来源（重建）==")
    print("fc_source:", dict(Counter(r["fc_source"] for r in rows)))
    print()
    print("== 修前 vs 修后：终局验证状态分布 ==")
    print("before:", dict(Counter(r["before"] for r in rows)))
    print("after :", dict(Counter(r["after"] for r in rows)))
    print()
    print("== 答案被认证（answer_verified）==")
    print("before:", dict(Counter(r["before_verified"] for r in rows)))
    print("after :", dict(Counter(r["after_verified"] for r in rows)))
    print()
    print("== 被降级条目（LLM 规格 + 原 PASS → 修后 UNSURE）==")
    for r in rows:
        if r["before"] != r["after"]:
            print(f"  #{r['id']:>2} 规格={r['fc_source']}  修前 {r['before']} → 修后 {r['after']}   "
                  f"答案认证 {r['before_verified']} → {r['after_verified']}")
    if not any(r["before"] != r["after"] for r in rows):
        print("  （无降级——历史运行中无 LLM 规格 PASS）")
    print()
    print("== 语义说明 ==")
    print("规则派生（L1 锚）的 PASS 不受影响；LLM 声明规格（L0 锚）的 PASS 是假认证（#8 根因），降级为诚实弃权。")


if __name__ == "__main__":
    main()
