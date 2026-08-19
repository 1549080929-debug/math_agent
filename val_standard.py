"""VAL 判级标准工具（docs/06-判级标准.md 的可运行版）。

用法：
    python val_standard.py              # 跑内置 10 用例自测
    python val_standard.py <anchor> <guarantee> [scope]   # 直接判级

代码中使用：
    from val_standard import classify
    level, note = classify("decidable", "completeness", "single")
"""

import sys

# ---------------------------------------------------------------------------
# 判级程序（docs/06 第 2 节）：顺序判断，先中先得
# ---------------------------------------------------------------------------


def classify(anchor, guarantee, scope=None):
    """判级三问 → (等级, 说明)。

    anchor:    "llm" | "rule" | "truth" | "decidable"   (Q1 规格来源)
    guarantee: "none" | "correctness" | "completeness"  (Q2 保证类型)
    scope:     "single" | "domain" | "universal"        (Q3 覆盖范围，仅完备性时用)
    """
    if guarantee == "completeness" and scope == "universal":
        return ("L5", "任意性质完备验证——无限制情形不可能（Rice 仅覆盖程序语义；经验命题/主观性质另两类），判级否决")
    if guarantee == "completeness" and scope == "domain":
        return ("L4", "领域级证明系统（类型系统全域/证明助手内核）")
    if guarantee == "completeness":
        return ("L3", "单性质完备：性质编码进可判定系统（ODD 内）")
    if guarantee == "correctness":
        if anchor == "decidable":
            return ("L2", "可判定系统只用于正确性——用法降级，可抬级到 L3")
        if anchor == "truth":
            return ("L2", "正确性 + 金标锚（独立客观真值/已知正确参照）")
        if anchor == "silver":
            return ("L1", "银锚：确定性重计算，客观于计算而非答案——L1/L2 边界，按作者判 L1")
        if anchor == "rule":
            return ("L1", "确定性规则，规格从题面/代码派生")
    return ("L0", "LLM 自证 / 无确定性锚（信任递归）")


CASES = [
    # (名称, anchor, guarantee, scope, 期望等级)
    ("LLM 自证'我检查过了'",          "llm",       "none",          None,       "L0"),
    ("题面正则提取 final_check",       "rule",      "correctness",   None,       "L1"),
    ("VerifiAgent 工具（银锚）",       "silver",    "correctness",   None,       "L1"),
    ("代回验证 verify_root",          "truth",     "correctness",   None,       "L2"),
    ("采样验证 final_parameter_set",   "truth",     "correctness",   None,       "L2"),
    ("solveset 但只代回（用法降级）",   "decidable", "correctness",   None,       "L2"),
    ("solveset 解集等价",             "decidable", "completeness",  "single",   "L3"),
    ("类型系统 answer_type",          "decidable", "completeness",  "single",   "L3"),
    ("Alvarado 决策规则",             "decidable", "completeness",  "single",   "L3"),
    ("Rust borrow checker",          "decidable", "completeness",  "domain",   "L4"),
    ("通用完备验证器（不存在）",        "decidable", "completeness",  "universal", "L5"),
]


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if argv:
        anchor = argv[0]
        guarantee = argv[1] if len(argv) > 1 else "correctness"
        scope = argv[2] if len(argv) > 2 else ("single" if guarantee == "completeness" else None)
        level, note = classify(anchor, guarantee, scope)
        print(f"{anchor}/{guarantee}/{scope} → {level} | {note}")
        return 0

    passed = 0
    for name, a, g, s, expect in CASES:
        level, note = classify(a, g, s)
        ok = "OK " if level == expect else "XX "
        passed += level == expect
        print(f"{ok}[{level}] {name}: {note}")
    print(f"\n=== VAL 判级标准自测：{passed}/{len(CASES)} 通过 ===")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
