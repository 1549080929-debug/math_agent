"""val_demo.py：工具链能力演示（判级 → 抬级 → 处方 → 体检）。

用法：python val_demo.py
"""
import sys

sys.path.insert(0, ".")

from val_standard import classify          # noqa: E402
from val_raise import prescribe, scan_anchor, audit_report  # noqa: E402


def show(title, s):
    print("\n" + "=" * 72)
    print("▶ " + title)
    print("=" * 72)
    print(s)


def main():
    # 1. 判级器：真实场景分类
    show("一、判级器：给任意验证方案贴等级（val_standard）", "")
    scenarios = [
        ("某 Agent 自评'输出已验证'", "llm", "none", None),
        ("RAG 知识库引用检查", "rule", "correctness", None),
        ("单元测试执行对比", "truth", "correctness", None),
        ("SymPy 解集等价", "decidable", "completeness", "single"),
        ("Rust borrow checker", "decidable", "completeness", "domain"),
    ]
    for name, a, g, s in scenarios:
        lvl, note = classify(a, g, s)
        print(f"  {name:<26} → {lvl}  {note}")

    # 2. 抬级器：处方 + 骨架 + 确认清单
    show("二、抬级器：处方、代码骨架、人工确认环（val_raise）", "")
    cases = [
        ("数学代回验证", True, "substitution", "solver"),
        ("医疗手写规则", True, "hand_rule", "decision_rule"),
        ("LLM 自评代码", True, "llm_judge", "type_system"),
        ("行为统计检测(隐匿执行)", False, "statistical", "none"),
    ]
    for name, e, m, a in cases:
        lvl, ok, pat, skel, confirms, msg = prescribe(e, m, a)
        print(f"\n  ◆ {name}")
        print(f"    等级={lvl}  可抬级={ok}  模式={pat}")
        if ok:
            print(f"    处方: {msg.split('例：')[0].strip()}")
            if skel:
                print("    代码骨架:")
                for ln in skel.splitlines():
                    print(f"      | {ln}")
            print(f"    确认清单: {confirms}")
        else:
            print(f"    边界（诚实拒绝）: {msg}")

    # 3. 可判定域扫描
    show("三、可判定域扫描（val_raise.scan_anchor）", "")
    for kind in ["equation", "clinical_pe", "behavior_covert"]:
        anchors = scan_anchor(kind)
        if anchors:
            for name, typ, comp, note in anchors:
                print(f"  {kind:<18} → {name}  [{typ}]  完备={comp} · {note}")
        else:
            print(f"  {kind:<18} → （无已知可判定锚 —— 诚实边界）")

    # 4. 审计报告
    show("四、验证栈体检（val_raise.audit_report）", "")
    stack = [("LLM 自评", "L0"), ("单元测试", "L2"), ("类型检查", "L3"),
             ("行为统计检测", "L2"), ("信息完整性裁判", "L2")]
    print(audit_report(stack))


if __name__ == "__main__":
    main()
