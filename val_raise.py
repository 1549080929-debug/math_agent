"""val_raise.py：L2→L3 抬级器（可行性判定 + 重编码处方）。

把 docs/06 的处方（"性质可编码 → 抬级到 L3"）从文档变成可运行工具。
输入一个验证方案的关键属性，输出：当前等级、抬级可行性、适用模式、具体处方；
或诚实的"无法抬级"（原理性边界）。

用法：
    python val_raise.py                    # 跑内置自测
    python val_raise.py <encodable> <method> <anchor>

参数：
    encodable: true | false | unknown   —— 性质能否编码进可判定系统
    method:    substitution | sampling | hand_rule | llm_judge | statistical | decidable_underused
    anchor:    solver | decision_rule | type_system | none | unknown —— 领域是否有已验证锚可导入
"""

import sys

PATTERNS = {
    "A": "解集等价重编码：把'代回验证候选'改为'求解完整解集并比较集合'（如 solveset）。",
    "B": "穷举/闭式重编码：把'抽样验证'改为'枚举有限候选空间/端点+驻点/约束求解'（若空间有限）。",
    "C": "导入已验证锚：把'手写规则'替换为领域已验证决策规则（如 Alvarado/Wells/PERC）。",
    "D": "确定性检查：把'LLM 判定'替换为机械可检查的检查器（类型系统/schema/编译器）。",
    "E": "用法抬级：可判定系统已存在但只用其正确性能力，改用其完备能力（solveset 替代代回）。",
    "F": "确定性特征替代：把'统计检测'替换为可判定的确定性特征/规则（若性质可编码）。",
}


def analyze(encodable, method, anchor):
    """返回 (等级, 可抬级, 模式, 处方或边界说明)。"""
    # 1) 性质不可编码 → 原理性边界（对应 L5 不可判定的现实投影）
    if encodable is False:
        return ("L2", False, "-",
                "性质不可编码进任何可判定系统——无法抬级（原理性边界，如'输出层无痕迹的攻击'）。"
                "诚实做法：保持 L2 并明确标注为正确性探针。")
    # 2) 可判定性未知 → 诚实要求人工确认
    if encodable is None:
        return ("L2", None, "?",
                "性质的可判定性未知——不能自动判定。需人工回答：该性质能否用闭式解/穷举/"
                "类型/决策规则表达？确认后才能抬级。")

    # 3) 可编码 → 按当前方法选择模式
    if method == "substitution":
        p = "A" if anchor == "solver" else "A"
        return ("L2", True, p, PATTERNS[p] + " 例：verify_root(代回) → solution_set(解集等价)。")
    if method == "sampling":
        return ("L2", True, "B", PATTERNS["B"] +
                " 例：区间最值端点+驻点穷举（二次函数域内完备）；若候选空间无限→只能部分抬级，标注采样天花板。")
    if method == "hand_rule":
        if anchor in ("decision_rule", "solver", "type_system"):
            return ("L1", True, "C", PATTERNS["C"] + " 例：手写'lab缺失+conf>0.6' → Alvarado 区间语义。")
        return ("L1", True, "C*", "手写规则可判定，但领域无已验证锚可导入——可抬级到 L3*，"
                "前提是规则本身经过外部验证；否则维持 L1/L2 并诚实标注。")
    if method == "llm_judge":
        if anchor in ("type_system", "solver"):
            return ("L0", True, "D", PATTERNS["D"] + " 例：LLM 自评代码 → 类型检查/编译。")
        return ("L0", False, "-",
                "LLM 判定 + 性质不可机械检查（如主观质量）→ 无法抬级；若性质其实可编码，"
                "先把性质表达成可判定形式（回到 encodable=true）。")
    if method == "statistical":
        if anchor in ("type_system", "solver"):
            return ("L2", True, "F", PATTERNS["F"] + " 例：统计检测 → 确定性特征/规则（若性质可编码）。")
        return ("L2", False, "-",
                "统计检测 + 无可判定锚可替代 → 无法抬级；保持 L2 并诚实标注（如行为检测的隐匿执行边界）。")
    if method == "decidable_underused":
        return ("L2", True, "E", PATTERNS["E"] + " 例：solveset 只做代回 → 用解集等价。")
    return ("L0", None, "?", "未知方法类型，无法自动判定。")


CASES = [
    # (名称, encodable, method, anchor, 期望可抬级 True/False/None)
    ("数学代回(verify_root)",     True,  "substitution",      "solver",        True),
    ("数学采样(final_param)",      True,  "sampling",           "solver",        True),
    ("医疗手写规则(信息完整性)",     True,  "hand_rule",          "decision_rule", True),
    ("行为隐匿执行(统计)",          False, "statistical",        "none",          False),
    ("LLM自评代码",               True,  "llm_judge",          "type_system",   True),
    ("solveset只代回(用法降级)",    True,  "decidable_underused", "solver",        True),
    ("性质可判定性未知",            None,  "substitution",       "solver",        None),
    ("手写规则无验证锚",            True,  "hand_rule",          "none",          True),
    ("LLM自评主观质量",            False, "llm_judge",           "none",          False),
    ("统计检测有可判定特征",        True,  "statistical",        "type_system",   True),
]


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if argv:
        enc = {"true": True, "false": False, "unknown": None}[argv[0].lower()]
        method, anchor = argv[1], argv[2]
        lvl, ok, pat, msg = analyze(enc, method, anchor)
        print(f"[{lvl}] 可抬级={ok} 模式={pat}\n  {msg}")
        return 0

    passed = 0
    for name, enc, method, anchor, expect in CASES:
        lvl, ok, pat, msg = analyze(enc, method, anchor)
        good = (ok == expect)
        passed += good
        print(f"{'OK ' if good else 'XX '}{name}: [{lvl}] 可抬级={ok} 模式={pat}"
              + (f" 期望={expect}" if not good else ""))
    print(f"\n=== val_raise 自测：{passed}/{len(CASES)} 通过 ===")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
