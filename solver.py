"""子任务求解器：带上下文传递的逐个求解 + 反馈纠错

对应对话中的关键设计：
- 上下文传递：前一个已验证的子任务结果，注入到下一个子任务的 Prompt，
  防止"后一个不知道前一个算出了什么"导致的组合矛盾。
- 反馈纠错（补丁 P2）：验证失败时，把验证器的报错回传给 LLM 让它修正。
"""

import json

from llm_client import chat_json

SOLVE_SYSTEM_PROMPT = """你是数学求解器。求解给定的子任务，只输出 JSON：
{"answer": "最终结果（精确值：分数/根号表达式，不要四舍五入）", "steps": "简要步骤（人类可读文本）"}
要求：
1. 直接使用上下文里已验证的前序结果，不要重新计算它们。
2. answer 必须是一个单一值（本系统暂不支持"多个解"形态，一个子任务只求一个量）。"""


def solve_subtask(question, subtask, context, constraints=None):
    """首次求解单个子任务。context: 已通过验证的前序结果 dict。"""
    context_text = json.dumps(context, ensure_ascii=False) if context else "（暂无）"
    constraints_text = ""
    if constraints:
        constraints_text = f"\n题目隐含约束（求解时必须遵守）：{json.dumps(constraints, ensure_ascii=False)}"
    data = chat_json([
        {"role": "system", "content": SOLVE_SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"原题：{question}\n\n"
            f"子任务：{subtask['task']}\n\n"
            f"已验证的前序结果：{context_text}\n"
            f"{constraints_text}\n\n"
            f"请求解。"
        )},
    ], temperature=0.2)
    return data


def fix_subtask(question, subtask, context, failed_result, verify_message, attempt, constraints=None):
    """反馈纠错：把验证器报错回传给 LLM，让它修正答案。"""
    constraints_text = ""
    if constraints:
        constraints_text = f"\n题目隐含约束（求解时必须遵守）：{json.dumps(constraints, ensure_ascii=False)}"
    data = chat_json([
        {"role": "system", "content": SOLVE_SYSTEM_PROMPT + "\n你现在是在修正一个未通过验证的答案。"},
        {"role": "user", "content": (
            f"原题：{question}\n\n"
            f"子任务：{subtask['task']}\n\n"
            f"你的上一次答案：{json.dumps(failed_result, ensure_ascii=False)}\n\n"
            f"验证器报错：{verify_message}\n\n"
            f"已验证的前序结果：{json.dumps(context, ensure_ascii=False)}\n"
            f"{constraints_text}\n\n"
            f"请修正（第 {attempt} 次修正）。"
        )},
    ], temperature=0.2)
    return data
