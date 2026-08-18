"""组合模块：把全部子结果组装成完整解答（按验证状态如实标注）

审计修正 1：combiner 逐条标注验证状态，禁止把 UNSURE 说成已验证。
审计修正 2：combiner 输出结构化 JSON {"answer": 规范答案, "text": 解题过程}——
  这样终局验证器能解析最终答案；失败时可带着报错重试，只改 answer。

对应对话中最关键的架构修正："根基坏了"的修复——
LLM 是自由文本生成器，组合阶段铁律：严禁重算、严禁把未验证说成已验证。
"""

import json

from llm_client import chat, chat_json

COMBINE_SYSTEM_PROMPT = """你是数学解答的组装者。以下子结果每一条都标注了验证状态：
- "已通过符号引擎验证"：可信事实，直接使用；
- "未能验证（裁判弃权）"：未经确认的内容，你必须如实标注"该步骤未经符号验证"，严禁声称其已验证。
输出 JSON：
{"answer": "最终答案的规范形式（如 '0<=a<=2'、'a=1 或 a=2'、'x=3'。必须是一个纯粹的数学集合/数值，禁止任何解释文字、禁止出现'但需排除''实际为'等短语）",
 "text": "完整解题过程（自然语言）"}
铁律：
1. 严禁重新计算、修改、推导任何已验证的数值或表达式。
2. 严禁把"未能验证"的内容说成"已验证"。
3. 严禁添加未经验证的中间结果或额外步骤。
4. answer 字段必须与 text 中的最终结论一致。"""

STATUS_LABEL = {
    "PASS": "已通过符号引擎验证",
    "UNSURE": "未能验证（裁判弃权）",
    "FAIL": "验证失败",
}


def combine(question, subtasks_with_results, retry_hint=None):
    """组装最终解答。返回 {"answer": ..., "text": ...}。"""
    items = [{
        "task": s["subtask"]["task"],
        "answer": s["result"].get("answer", ""),
        "verification": STATUS_LABEL.get(s["verify"].status, s["verify"].status),
    } for s in subtasks_with_results]

    payload = json.dumps(items, ensure_ascii=False, indent=2)
    user_msg = (f"原题：{question}\n\n"
                f"子结果（按依赖顺序，含验证状态）：\n{payload}\n\n"
                f"请组装成完整解答。")
    if retry_hint:
        user_msg += f"\n\n【终局验证失败，请修正】{retry_hint}\n只修正 answer 字段（和 text 中对应的结论），不要重做子任务。"

    data = chat_json([
        {"role": "system", "content": COMBINE_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ], temperature=0.2, max_tokens=2000)

    if isinstance(data, dict) and data.get("answer"):
        return {"answer": str(data.get("answer", "")).strip(),
                "text": str(data.get("text", ""))}
    # 兜底：非 JSON 输出则原样作为 text
    return {"answer": "", "text": str(data)}
