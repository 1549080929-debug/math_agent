"""val_interrogate.py：追问层（P5）——把"自由文本声称 → 判级参数"的追问自动化。

设计纪律（自我指涉，docs/09 P5）：
- 追问用**确定性模板**（不是 LLM 生成的问题）——否则追问层自己就是 L0；
- 每个回答记录来源（声称者声明 = L0 输入），输出是"按这些声称的判级"，可审计；
- 答"不清楚" → 不猜，要求澄清/升级；
- **buzzword 不豁免**：区块链/共识/多智能体/分布式/投票 → 强制追问"聚合对象"。

用法：
    python val_interrogate.py            # 交互模式（对声称施加压力）
    python val_interrogate.py --auto     # 跑 5 道压力测试题（自测）
"""

import sys

sys.path.insert(0, ".")

from val_standard import classify          # noqa: E402
from val_raise import analyze, scan_anchor  # noqa: E402

# ---------------------------------------------------------------------------
# 声称探测：确定性关键词 → 追问提示（buzzword 不豁免）
# ---------------------------------------------------------------------------
PATTERNS = [
    (["自评", "自查", "自己检查", "我检查过", "自我验证", "反思"], "⚠ 检测到'LLM 自证'语义——追问：验证条件由谁声明？"),
    (["区块链", "共识", "分布式", "多智能体", "投票", "互相检查", "互相验证"],
     "⚠ buzzword 检测：'分布式/共识' ≠ 确定性。追问：① 节点聚合的是什么——LLM 判断还是确定性锚输出？"
     "② '不可篡改'保证的是记录完整性还是判定正确性？"),
    (["SymPy", "符号", "solver", "求解器"], "⚠ 检测到可判定系统（solver）。追问：怎么用的——代回（L2）还是解集等价（L3）？"),
    (["单元测试", "测试", "golden", "金标", "基准"], "⚠ 检测到客观真值（测试/金标）。追问：保证'正确'还是'没有遗漏'？"),
    (["类型检查", "mypy", "编译", "type checker"], "⚠ 检测到类型系统（L3 锚）。追问：覆盖所有代码路径吗（ODD）？"),
    (["规则引擎", "正则", "schema", "校验"], "⚠ 检测到确定性规则。追问：规则本身经过外部验证吗（L3*）？"),
    (["优雅", "美观", "质量好", "可读性好"], "⚠ 检测到主观性质。追问：能编码进可判定系统吗？还是只能人工评？"),
    (["形式化", "证明", "Lean", "Coq", "验证器"], "⚠ 检测到形式化验证。追问：定理陈述由谁声明（LLM → L0 陈述层）？"),
]


def probe(claim):
    """对声称文本做确定性探测，返回追问提示列表。"""
    hits = []
    for kws, hint in PATTERNS:
        if any(k in (claim or "") for k in kws):
            hits.append(hint)
    return hits or ["（未检测到已知模式——直接进入标准三问）"]


# ---------------------------------------------------------------------------
# 判级 + 抬级组合（给定结构化回答）
# ---------------------------------------------------------------------------
SPECS = {"llm": "LLM 声明", "rule": "题面/代码规则", "truth": "客观真值", "decidable": "可判定系统"}
GUARANTEES = {"none": "无", "correctness": "正确性", "completeness": "完备性"}
METHODS = {"substitution": "代回", "sampling": "采样", "hand_rule": "手写规则",
           "llm_judge": "LLM 判定", "statistical": "统计", "decidable_underused": "可判定但只用正确性"}
ANCHORS = {"solver": "求解器", "decision_rule": "决策规则", "type_system": "类型系统", "none": "无"}


def classify_from_answers(spec, guarantee, scope, encodable, method, anchor):
    """组合判级器 + 抬级器：返回 (等级, 可抬级, 模式, 判级说明, 抬级说明)。"""
    lvl, note = classify(spec, guarantee, scope)
    lvl_r, ok, pat, msg = analyze(encodable, method, anchor)
    anchors = scan_anchor(_kind_of(claim_guess=""))  # 占位，见下方 kind 推断
    return lvl, ok, pat, note, msg


def _kind_of(encodable, anchor):
    # 简化：由 anchor 参数反推可判定域类型（用于扫描展示）
    return {"solver": "equation", "decision_rule": "clinical_appendicitis",
            "type_system": "type"}.get(anchor, "unknown")


# ---------------------------------------------------------------------------
# 交互模式：对声称施加压力
# ---------------------------------------------------------------------------
def _ask(question, options):
    print("\n" + question)
    for i, o in enumerate(options, 1):
        print(f"  {i}) {o}")
    while True:
        ans = input("  回答(数字/字母) > ").strip().lower()
        if ans in [str(i) for i in range(1, len(options) + 1)]:
            return options[int(ans) - 1]
        if ans in "abcd":
            return ans
        print("  （请重新输入）")


def interactive():
    claim = input("请输入验证声称（或直接回车跳过）> ").strip()
    print("\n===== 声称探测 =====")
    for h in probe(claim):
        print("  " + h)
    print("\n===== 判级三问（确定性问题模板）=====")
    spec = _ask("Q1 验证条件（规格）由谁声明？",
                ["被测 LLM 自己", "题面/代码确定性规则", "独立客观真值/金标", "性质编码进可判定系统", "不清楚"])
    if spec == "不清楚":
        print("  不猜——请先澄清：验证条件到底由谁写？没有答案前无法判级。")
        return
    spec_key = {"被测 LLM 自己": "llm", "题面/代码确定性规则": "rule",
                "独立客观真值/金标": "truth", "性质编码进可判定系统": "decidable"}[spec]
    guar = _ask("Q2 PASS 保证什么？", ["无（只是声明）", "正确性（提出的候选都成立）", "完备性（没有候选被遗漏）", "不清楚"])
    if guar == "不清楚":
        print("  不猜——请澄清保证类型；若连保证什么都说不清，建议按'无'保守判级。")
        return
    guar_key = {"无（只是声明）": "none", "正确性（提出的候选都成立）": "correctness",
                "完备性（没有候选被遗漏）": "completeness"}[guar]
    scope_key = None
    if guar_key == "completeness":
        scope = _ask("Q3 完备性覆盖多大范围？", ["单个性质", "整个领域", "声称任意性质", "不清楚"])
        if scope == "不清楚":
            print("  不猜——完备性声明必须给出范围。")
            return
        scope_key = {"单个性质": "single", "整个领域": "domain", "声称任意性质": "universal"}[scope]

    print("\n===== 抬级追问 =====")
    enc = _ask("Q4 该性质能编码进可判定系统吗？", ["能（有求解器/类型/决策规则可表达）", "不能（主观/不可判定）", "不确定"])
    enc_key = {"能（有求解器/类型/决策规则可表达）": True, "不能（主观/不可判定）": False, "不确定": None}[enc]
    method = _ask("Q5 当前验证方法是什么？",
                  ["代回/单点检查", "采样", "手写规则", "LLM 判定", "统计检测", "可判定系统但只用正确性"])
    method_key = {"代回/单点检查": "substitution", "采样": "sampling", "手写规则": "hand_rule",
                  "LLM 判定": "llm_judge", "统计检测": "statistical",
                  "可判定系统但只用正确性": "decidable_underused"}[method]
    anchor = _ask("Q6 领域有可导入的已验证锚吗？", ["求解器", "决策规则", "类型系统", "无", "不确定"])
    anchor_key = {"求解器": "solver", "决策规则": "decision_rule", "类型系统": "type_system",
                  "无": "none", "不确定": "unknown"}[anchor]

    lvl, ok, pat, note, msg = _final(spec_key, guar_key, scope_key, enc_key, method_key, anchor_key)
    print("\n" + "=" * 60)
    print(f"判级: {lvl}  |  {note}")
    print(f"抬级: 可抬级={ok}  模式={pat}")
    print(f"       {msg}")
    print("=" * 60)
    print("（注：以上基于你声明的回答——声称是 L0 输入，工具不验证其真实性）")


def _final(spec, guar, scope, encodable, method, anchor):
    lvl, note = classify(spec, guar, scope)
    _, ok, pat, msg = analyze(encodable, method, anchor)
    return lvl, ok, pat, note, msg


# ---------------------------------------------------------------------------
# 自动模式：5 道压力测试题（自测）
# ---------------------------------------------------------------------------
AUTO = [
    # (题, spec, guar, scope, encodable, method, anchor, 期望等级)
    ("多智能体互检+投票(节点=LLM)", "llm", "none", None, True, "llm_judge", "none", "L0"),
    ("SymPy 但只代回", "decidable", "correctness", None, True, "decidable_underused", "solver", "L2"),
    ("SymPy 解集等价", "decidable", "completeness", "single", True, "substitution", "solver", "L3"),
    ("验证代码'优雅'(LLM评)", "llm", "none", None, False, "llm_judge", "none", "L0"),
    ("区块链共识(节点=LLM)", "llm", "none", None, True, "llm_judge", "none", "L0"),
]


def auto_test():
    passed = 0
    print("===== 追问层自测：5 道压力测试题 =====")
    for claim, spec, guar, scope, enc, method, anchor, expect in AUTO:
        lvl, ok, pat, note, msg = _final(spec, guar, scope, enc, method, anchor)
        good = lvl == expect
        passed += good
        hints = probe(claim)
        print(f"\n{'OK ' if good else 'XX '}题: {claim}")
        for h in hints:
            print(f"      {h}")
        print(f"    → {lvl}  可抬级={ok}  模式={pat}  (期望 {expect})")
    print(f"\n=== 追问层自测：{passed}/{len(AUTO)} 通过 ===")
    return 0 if passed == len(AUTO) else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        raise SystemExit(auto_test())
    interactive()
