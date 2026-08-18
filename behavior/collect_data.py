"""收集固定探针行为数据：正常/注入/模糊 条件下的响应（增量保存）。

审计先行：先建带标签基线集（已知攻击 + 正常 + 模糊），
再测"行为统计是否可分"——价值窗口实测，窗口为空就止损。
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_client import chat  # noqa: E402

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_raw.json")


def build_prompts():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probes.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    tasks = []
    for probe in cfg["probes"]:
        for cond, spec in cfg["conditions"].items():
            for i in range(spec["samples"]):
                tasks.append({"probe": probe, "condition": cond, "sample": i,
                              "prompt": spec["template"].format(probe=probe)})
        # 留出注入类型（未知攻击模拟）
        for i in range(2):
            tasks.append({"probe": probe, "condition": "injectD", "sample": i,
                          "prompt": cfg["holdout_injection"]["injectD"].format(probe=probe)})
    return tasks


def main():
    tasks = build_prompts()
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            done = json.load(f)
        done_keys = {(d["probe"], d["condition"], d["sample"]) for d in done}
    except Exception:
        done, done_keys = [], set()

    for t in tasks:
        key = (t["probe"], t["condition"], t["sample"])
        if key in done_keys:
            continue
        try:
            text = chat([{"role": "user", "content": t["prompt"]}], temperature=0.7, max_tokens=800)
        except Exception as e:
            text = f"[采集异常] {e}"
        done.append({**t, "response": text})
        done_keys.add(key)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(done, f, ensure_ascii=False, indent=1)

    from collections import Counter
    cnt = Counter(d["condition"] for d in done)
    print(f"完成 {len(done)} 条：{dict(cnt)}")
    print(f"已保存 {DATA_FILE}")


if __name__ == "__main__":
    main()
