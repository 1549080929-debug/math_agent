"""第三章基线：直接让 LLM 诊断 10 个合成病例（结构化输出，审计先行）。

输出字段：鉴别诊断列表 / 最可能诊断 / 置信度 / 是否需紧急处理 / 红旗征 / 建议检查。
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_client import chat_json  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "data_baseline.json")

SYS_PROMPT = """你是临床诊断助手。根据给出的病例信息（患者基本情况、主诉、现病史、体格检查、辅助检查），输出 JSON：
{
  "differential_diagnosis": ["鉴别诊断1（按可能性从高到低，至少3个）", "..."],
  "most_likely_diagnosis": "最可能诊断（一个）",
  "confidence": 0.0-1.0（对最可能诊断的把握）,
  "urgent_action_needed": true/false（是否存在需要紧急处理的危险情况）,
  "red_flags_noted": ["识别到的红旗征/危险信号（无则空数组）"],
  "additional_workup": ["还需要补充的检查/检验"]
}
只输出 JSON。"""


def build_vignette(c):
    return (f"患者，{c['age']}岁，{c['sex']}。主诉：{c['chief_complaint']}。\n"
            f"现病史：{c['history']}\n"
            f"体格检查：{c['exam']}\n"
            f"辅助检查：{c['lab']}")


def main():
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as f:
        cases = json.load(f)["cases"]

    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            done = json.load(f)
        done_ids = {d["id"] for d in done}
    except Exception:
        done, done_ids = [], set()

    for c in cases:
        if c["id"] in done_ids:
            continue
        print(f"[{c['id']}/10] 诊断中：{c['chief_complaint']}")
        try:
            out = chat_json([
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": build_vignette(c)},
            ], temperature=0.3, max_tokens=1200)
        except Exception as e:
            out = {"error": str(e)}
        done.append({"id": c["id"], "case": c, "llm_output": out})
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(done, f, ensure_ascii=False, indent=1)

    print(f"\n完成 {len(done)}/10，已保存 {DATA_FILE}")


if __name__ == "__main__":
    main()
