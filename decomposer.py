"""拆解模块：入口分类（初段判断）+ 子任务拆解 + 拆解自查

对应对话中的关键设计：
- 初段分类 = 给题目打"数学血统"标签（学科权重），决定走哪条解题路线
- 拆解 = 把综合题拆成可独立验证的子任务（含依赖关系 DAG）
- 自查 = 把拆解结果和原题一起发回 LLM 检查完备性（对话中你确认过的方案）
"""

import json

from llm_client import chat_json

# ---- 补丁 P1：规则复核（关键词级别的粗略自洽检查） ----
APPLIED_KEYWORDS = [
    "价格", "利润", "面积", "体积", "时间", "速度", "池", "水",
    "篱笆", "商品", "成本", "销售", "米", "元", "秒", "分钟", "小时", "长", "宽",
]


def rule_check_classification(question, cls):
    """基于关键词的粗略复核，返回 (ok, 原因)。"""
    issues = []
    ct = cls.get("context_type", "")
    if ct == "applied" and not any(k in question for k in APPLIED_KEYWORDS):
        issues.append("context_type=applied 但题干中没有实际情境关键词")
    if ct == "pure_algebra" and any(k in question for k in APPLIED_KEYWORDS):
        issues.append("context_type=pure_algebra 但题干中出现了情境关键词")
    return (len(issues) == 0, "；".join(issues) if issues else "ok")


CLASSIFY_PROMPT = """你是数学题入口分类器。输出 JSON，字段含义：
{
  "context_type": "pure_algebra（纯代数） / geometry（几何结合） / applied（实际应用）",
  "complexity_level": "B1（单操作） / B2（双操作） / B3（综合含参多步）",
  "math_weight": {"algebra": 0~1, "geometry": 0~1, "arithmetic": 0~1, "calculus": 0~1},
  "required_operations": ["如 find_extreme_on_interval / solve_parameter / find_roots / find_vertex ..."],
  "constraints": {"x": ">0", "a": "任意实数"},
  "verification_hint": "用 SymPy 求导并检查端点"
}
math_weight 表示这道题在数学各分支上的"血统占比"，总和应为 1。"""


def classify(question):
    """第1步：入口分类。LLM 输出数学身份 + 核心操作 + 隐含约束。"""
    cls = chat_json([
        {"role": "system", "content": CLASSIFY_PROMPT},
        {"role": "user", "content": f"请分类这道题：\n{question}"},
    ], temperature=0.3)
    ok, reason = rule_check_classification(question, cls)
    if not ok:
        # 规则复核不过 → 让 LLM 重新分类一次
        cls = chat_json([
            {"role": "system", "content": CLASSIFY_PROMPT + f"\n上次分类存在自洽性问题：{reason}，请修正。"},
            {"role": "user", "content": f"请重新分类这道题：\n{question}"},
        ], temperature=0.3)
    return cls


DECOMPOSE_PROMPT = """你是数学题拆解专家。把题目拆成 2-5 个可独立验证的子任务，输出 JSON：
{
  "subtasks": [
    {
      "id": 1,
      "task": "子任务描述（明确写出要算出的量）",
      "weight": 0~1,
      "type": "value|interval|point_set|union|inequality（本子任务答案的类型，必须与实际答案一致）",
      "verify": {"type": "root|extreme|interval_extreme|equality|satisfies|inequality", "params": {...}},
      "depends_on": [前置子任务 id 列表]
    }
  ],
  "final_check": {
    "type": "final_parameter_set",
    "params": {
      "expr": "含参数 a 的表达式，如 x**2 - 2*a*x + 1",
      "var_name": "x",
      "param_name": "a",
      "interval": ["0", "2"],
      "conditions": [{"which": "min|max|diff", "op": ">=|<=|==", "value": "0"}]
    }
  }
}
final_check 用于终局验证最终答案（参数集合）：在声称的集合内抽样，检查区间上 min/max/diff 是否满足条件。
例如"最小值不小于0 且 最大值不超过5" → conditions: [{"which":"min","op":">=","value":"0"},{"which":"max","op":"<=","value":"5"}]。
若最终答案不是参数集合（如单个数值），final_check 输出 null。

验证类型说明：
- root:       验证求根。params: {"equation": "x**2 - 5*x + 6", "var_name": "x"}（root 取本子任务答案）
- extreme:    验证驻点。params: {"expr": "x**2 - 4*x + 7", "var_name": "x"}（point 取本子任务答案）
- interval_extreme: 验证区间最值。params: {"expr": "...", "var_name": "x",
              "interval": ["0", "2"], "which": "min|max", "claimed": "-1",
              "subs": {"a": "<answer>"}}（claimed 和 subs 里的 <answer> 会被替换为本子任务答案）
- equality:   验证表达式等价。params: {"expr1": "..."}（expr2 取本子任务答案）
- satisfies:  验证满足条件。params: {"condition": "x > 0 或 1 <= x <= 4", "var_name": "x"}（value 取本子任务答案）
- inequality: 验证不等式解集。params: {"condition": "(k+2)**2 - 4 < 0 或 8*m - 4 > 0", "var_name": "k"}
              （claimed 取本子任务答案，支持 "(-4, 0)"、"m > 1/2"、"0 <= a <= 2"、"a = 0 或 a = 2" 等形态）

规则：
1. 每个子任务必须能单独被 SymPy 验证（这是铁律，无法验证就不要拆出来）。
2. 写明依赖关系：哪个子任务的结果被哪个后续子任务使用。
3. weight 表示"这一步出错对最终结果的影响度"，总和应为 1。
4. 含参问题（如"求参数 a"）用 interval_extreme + subs 模式：把 a 代回再验最值。
5. type 必须诚实：答案是区间就写 interval，是离散点就写 point_set，不能混淆。"""


def decompose(question, cls):
    """第2步：拆解子任务。返回 (subtasks, final_check)。"""
    context = json.dumps({"入口分类": cls}, ensure_ascii=False)
    data = chat_json([
        {"role": "system", "content": DECOMPOSE_PROMPT},
        {"role": "user", "content": f"题目：\n{question}\n\n入口分类：\n{context}\n\n请拆解。"},
    ], temperature=0.3, max_tokens=3000)
    if isinstance(data, list):
        return data, None
    return data.get("subtasks", []), data.get("final_check")


SELF_CHECK_PROMPT = """你是拆解质检员。检查拆解是否：
1) 覆盖题目所有条件（有没有遗漏的隐含约束，如定义域、正数、参数范围）；
2) 子任务依赖关系正确（depends_on 是否准确）；
3) 每个子任务都能被 SymPy 独立验证。
输出 JSON：{"ok": true/false, "issues": ["问题1", "问题2"], "fixed_subtasks": [修正后的完整子任务列表（仅当 ok=false 时提供）]}"""


def self_check(question, subtasks):
    """第3步：拆解自查。把拆解结果和原题一起发回 LLM，检查完备性。"""
    review = chat_json([
        {"role": "system", "content": SELF_CHECK_PROMPT},
        {"role": "user", "content": f"原题：\n{question}\n\n拆解结果：\n{json.dumps(subtasks, ensure_ascii=False)}\n\n请检查。"},
    ], temperature=0.2, max_tokens=3000)
    if not review.get("ok", False) and review.get("fixed_subtasks"):
        return review["fixed_subtasks"], review.get("issues", [])
    return subtasks, review.get("issues", [])
