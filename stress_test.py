"""5 道压力测试题：跑判级器/抬级器/扫描/体检。"""
import sys
sys.path.insert(0, ".")

from val_standard import classify
from val_raise import analyze, prescribe, scan_anchor, audit_report


def run(q, mapping, extras=""):
    print("\n" + "=" * 72)
    print("题: " + q)
    print("追问: " + mapping["probe"])
    print("-" * 72)
    for name, args in mapping["runs"]:
        lvl, note = classify(*args)
        print(f"  分支[{name}]: → {lvl}  {note}")
    if extras:
        print(extras)


# 题 1：多智能体互检 + 投票
run(
    "我们的系统使用多智能体验证，每个智能体互相检查，最终投票决定。",
    {
        "probe": "① 智能体互相检查时，'检查的规格'是谁声明的？② 投票聚合的是什么——LLM 判断还是工具输出？",
        "runs": [
            ("A: 节点是LLM，投票聚合LLM判断", ("llm", "none", None)),
            ("B: 节点是LLM，但检查对象是确定性工具输出", ("truth", "correctness", None)),
        ],
    },
    "  关键：投票不抬级。多个 L0 聚合 = 统计自一致性，仍是 L0；只有当投票聚合的是确定性锚的输出才到 L2。",
)

# 题 2：SymPy 验证所有数学答案
run(
    "我们用 SymPy 验证所有数学答案。",
    {
        "probe": "SymPy 怎么用的？① 代回单根（只用正确性能力）还是 ② 解集等价（用完备能力）？",
        "runs": [
            ("A: 只代回（用法降级）", ("decidable", "correctness", None)),
            ("B: 解集等价", ("decidable", "completeness", "single")),
        ],
    },
)

# 题 3：验证代码是否'优雅'
run(
    "验证一段代码是否'优雅'。",
    {
        "probe": "① '优雅'能编码进可判定系统吗？② 有没有可量化的代理（圈复杂度/LOC——但那是代理，不是'优雅'本体）？",
        "runs": [
            ("A: LLM 评'优雅'（主观）", ("llm", "none", None)),
            ("B: 规则打分（代理指标）", ("rule", "correctness", None)),
        ],
    },
    "  可判定域扫描: " + str(scan_anchor("elegance") or "（无已知可判定锚——性质本体不可编码，只能人工评）"),
)

# 题 4：工业级混合系统
print("\n" + "=" * 72)
print("题: 自动驾驶感知=CNN(L2统计)，决策=规则引擎(L1)，整体安全=形式化验证(L4)")
print("追问: ① L4 形式化验证覆盖的是什么——整个闭环还是某个模块？② 感知的错误能否被 L4 纳入其 ODD？")
print("-" * 72)
print(audit_report([("CNN 感知模块", "L2"), ("规则引擎决策", "L1"), ("整体安全(形式化验证)", "L4")]))
print("  关键: 系统整体等级 ≠ 最高模块等级。若 L4 只覆盖决策，感知的完备性盲区(L2)")
print("  会穿透到整体声称之上——整体受'最弱且不可抬的环节'约束。")

# 题 5：区块链 buzzword
run(
    "我们的验证器基于'区块链共识机制'，分布式节点共同确认结果，不可篡改。",
    {
        "probe": "① '共识'聚合的是什么——LLM 判断还是确定性锚的输出？② '不可篡改'保证的是记录完整性，还是判定正确性？",
        "runs": [
            ("A: 节点是LLM（buzzword穿透后）", ("llm", "none", None)),
            ("B: 节点执行确定性规则", ("rule", "correctness", None)),
        ],
    },
    "  关键: 区块链是'记账的锚'，不是'判定的锚'。不可篡改≠正确；分布式≠确定性。"
    " 若节点是 LLM，'共识' = 多个 L0 自证 = 仍是 L0。",
)
