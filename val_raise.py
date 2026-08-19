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


# ---------------------------------------------------------------------------
# P2: 可判定域自动扫描（性质类型 → 可用可判定锚）
# ---------------------------------------------------------------------------
ANCHOR_REGISTRY = {
    "equation":    [("SymPy solveset", "solver", True, "单变量代数方程，Reals 域解集等价")],
    "inequality":  [("SymPy solveset(Reals)", "solver", True, "一元不等式解集")],
    "extreme":     [("solve(deriv)+端点", "solver", True, "二次函数域内完备")],
    "type":        [("mypy/pyright", "type_system", True, "类型错误判定")],
    "syntax":      [("编译器/parser", "type_system", True, "语法判定")],
    "clinical_appendicitis": [("Alvarado (MANTRELS)", "decision_rule", True, "8 项客观输入+区间缺数据语义")],
    "clinical_pe":     [("Wells / PERC", "decision_rule", True, "PE 风险分层 / 排除规则")],
    "clinical_pneu":   [("CURB-65", "decision_rule", True, "肺炎严重度分层")],
    "clinical_chest":  [("HEART", "decision_rule", True, "胸痛风险分层")],
    "behavior_covert": [],   # 输出层无痕迹攻击：不可编码，无锚——诚实空列表
}


def scan_anchor(kind):
    """返回某性质类型的可用可判定锚列表；空列表 = 无已知锚（诚实边界）。"""
    return ANCHOR_REGISTRY.get(kind, [])


def has_anchor(kind):
    return bool(scan_anchor(kind))


# ---------------------------------------------------------------------------
# P3: 半自动重编码（处方 + 代码骨架 + 人工确认环）
# ---------------------------------------------------------------------------
SKELETONS = {
    "A": ("def verify_solution_complete(expr, claimed, var):\n"
          "    true_set = sp.solveset(expr, var, domain=sp.S.Reals)\n"
          "    claimed_set = _parse_solution_set(claimed, var)\n"
          "    return 'PASS' if true_set == claimed_set else 'FAIL'\n",
          ["确认性质是'求所有解'而非单点", "确认求解器 ODD 覆盖目标方程类",
           "确认 claimed 解析器支持答案形态（集合/区间/点集）"]),
    "B": ("def verify_exhaustive(expr, var, candidates):\n"
          "    # 穷举有限候选空间（端点/驻点/约束解）\n"
          "    all_candidates = closed_form_candidates(expr, var)\n"
          "    return 'PASS' if set(claimed) <= set(all_candidates) else 'FAIL'\n",
          ["确认候选空间有限（否则采样天花板）", "确认闭式解覆盖全部候选"]),
    "C": ("def check_validated_rule(case, llm_out):\n"
          "    mn, mx, missing = validated_rule_range(case)  # 如 alvarado.alvarado_range\n"
          "    # 缺数据 → 区间语义：规则拒绝完整打分\n"
          "    return verdict_by_range(mn, mx, llm_out)\n",
          ["确认所选规则是领域已验证规则（有外部文献背书）", "确认输入字段与规则八项对齐",
           "确认缺数据语义（区间）已实现而非硬编码阈值"]),
    "D": ("def check_type_feedback(code, header):\n"
          "    errs = mypy_check(code, header)  # L3 锚：类型检查器\n"
          "    return 'PASS' if not errs else ('REPAIR', errs)\n",
          ["确认性质机械可检查（类型/schema/语法）", "确认检查器输出可解析为反馈"]),
    "E": ("# 用法抬级：可判定系统已存在，改用其完备能力\n"
          "verify_root(代回) → verify_solution_set(解集等价)\n",
          ["确认可判定系统已可用（零新依赖）", "确认旧调用方迁移到新 API"]),
    "F": ("def detect_deterministic(features, rule):\n"
          "    return rule(features)  # 确定性规则替代统计阈值\n",
          ["确认性质可编码为确定性特征", "确认规则边界可判定（否则退回统计+L2标注）"]),
}


def prescribe(encodable, method, anchor):
    """P3：返回 (等级, 可抬级, 模式, 代码骨架, 人工确认清单)。"""
    lvl, ok, pat, msg = analyze(encodable, method, anchor)
    if not ok:
        return (lvl, False, pat, "", [], msg)
    skel, confirms = SKELETONS.get(pat, ("", []))
    return (lvl, True, pat, skel, confirms, msg)


# ---------------------------------------------------------------------------
# P4: 评测审计报告（嵌入 Agent 评测流程的产物）
#   两维显示：验证强度 × 规格置信（回应"高等级但对象可能错"的误读，docs/10 补刀 C）
# ---------------------------------------------------------------------------
RISK = {"L0": "高（无保证）", "L1": "高（规则匹配）", "L2": "中（正确性探针）",
        "L3": "低（ODD 内完备）", "L4": "低（域内完备）", "L5": "否决（不可判定）"}

SPEC_CONF = {"anchored": "有独立锚", "claimed": "仅声称(L0)", "unknown": "未标注"}


def audit_report(entries):
    """entries: [(name, level)] 或 [(name, level, spec_conf)] → 两维审计报告。

    spec_conf: "anchored"(规格有独立锚) / "claimed"(规格仅声称) / "unknown"(未标注)。
    """
    lines = ["# 验证栈审计报告（验证强度 × 规格置信）", "",
             "| 验证器/指标 | 强度 | 规格置信 | 风险 | 抬级建议 |",
             "|---|---|---|---|---|"]
    for e in entries:
        name, lvl = e[0], e[1]
        conf = e[2] if len(e) > 2 else "unknown"
        conf_txt = SPEC_CONF.get(conf, conf)
        pat, sug = ("-", "无") if lvl in ("L3", "L4") else ("E", "接入抬级器（val_raise）")
        lines.append(f"| {name} | {lvl} | {conf_txt} | {RISK.get(lvl, '?')} | {sug} |")
    lines.append("")
    lines.append("> 生成：val_raise.audit_report() —— 两维：强度=验证机制承诺什么，"
                 "规格置信=被验证的性质本身有没有独立锚（docs/10 补刀 C）。")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 补刀 B：ODD 自身分级（auxiliary dimension，docs/10）
#   ODD 从"能力约束"进一步：ODD 的锚也有等级
# ---------------------------------------------------------------------------
ODD_LEVELS = {
    "self_declared": ("L0", "使用者声称（'我的 ODD 是简单方程'）——无独立锚，免责条款风险"),
    "documented":    ("L1", "工具文档声称（'SymPy 支持 X'）——锚在文档，文档本身是声明"),
    "empirically_tested": ("L2", "在覆盖该域的基准上实测——锚在金标"),
    "formally_characterized": ("L3", "形式化刻画（类型可靠性证明/代数域）——锚在定义性"),
}


def odd_level(odd_type):
    """返回 ODD 声明的锚定等级（self_declared/documented/empirically_tested/formally_characterized）。"""
    return ODD_LEVELS.get(odd_type, ("?", "未知 ODD 类型"))


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

    # P2/P3/P4 自测
    more = [
        ("scan equation 有锚", scan_anchor("equation") != []),
        ("scan behavior_covert 无锚(诚实)", scan_anchor("behavior_covert") == []),
        ("scan clinical_pe 有 Wells/PERC", any("Wells" in a[0] for a in scan_anchor("clinical_pe"))),
        ("prescribe 返回骨架", "solveset" in prescribe(True, "substitution", "solver")[3]),
        ("prescribe 不可抬级(诚实)", prescribe(False, "statistical", "none")[1] is False),
        ("prescribe 有确认清单", len(prescribe(True, "hand_rule", "decision_rule")[4]) >= 3),
        ("audit_report 产出表格", "| 验证器" in audit_report([("root", "L2"), ("solution_set", "L3")])),
        ("audit_report 风险标注", "高（无保证）" in audit_report([("self_check", "L0")])),
        ("audit_report 两维(规格置信列)", "规格置信" in audit_report([("x", "L3", "anchored")])),
        ("audit_report 兼容二元组", audit_report([("x", "L2")]).count("|") > 0),
        ("odd_level self_declared=L0", odd_level("self_declared")[0] == "L0"),
        ("odd_level formally=L3", odd_level("formally_characterized")[0] == "L3"),
    ]
    for name, ok in more:
        passed += ok
        print(f"{'OK ' if ok else 'XX '}{name}")
    total = len(CASES) + len(more)
    print(f"\n=== val_raise 自测：{passed}/{total} 通过 ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
