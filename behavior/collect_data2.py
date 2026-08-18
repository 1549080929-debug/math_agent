"""第二轮数据采集：FPR 多样正常 / 攻击强度 / 对抗规避 / 基线漂移（增量保存）。"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_client import chat  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "data_raw2.json")


def build_tasks():
    with open(os.path.join(HERE, "probes2.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    tasks = []
    # FPR 多样正常
    for q in cfg["normal_diverse"]:
        tasks.append({"condition": "normal_diverse", "prompt": q, "sample": 0, "note": "FPR"})
    # 攻击强度（injectA 弱/中/强）
    for name, spec in cfg["intensity"].items():
        for probe in cfg["probes"]:
            for i in range(spec["samples"]):
                tasks.append({"condition": name, "prompt": spec["template"].format(probe=probe),
                              "sample": i, "note": "intensity"})
    # 对抗规避
    for name, tmpl in cfg["evasive"].items():
        for probe in cfg["probes"]:
            for i in range(2):
                tasks.append({"condition": name, "prompt": tmpl.format(probe=probe),
                              "sample": i, "note": "evasive"})
    # 基线漂移（英文回答 = 模拟模型更新后的正常行为）
    for probe in cfg["probes"]:
        for i in range(cfg["drift"]["samples"]):
            tasks.append({"condition": "drift_english",
                          "prompt": cfg["drift"]["template"].format(probe=probe),
                          "sample": i, "note": "drift"})
    return tasks


def main():
    tasks = build_tasks()
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            done = json.load(f)
        done_keys = {(d["condition"], d["prompt"], d["sample"]) for d in done}
    except Exception:
        done, done_keys = [], set()

    for t in tasks:
        key = (t["condition"], t["prompt"], t["sample"])
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
    print(f"完成 {len(done)} 条：{dict(Counter(d['condition'] for d in done))}")
    print(f"已保存 {DATA_FILE}")


if __name__ == "__main__":
    main()
