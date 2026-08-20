"""检查实验结果：逐场景打印 LLM 提议 + 防御裁决。"""
import io
import json
import sys

for cfg in ["D1", "D2", "D3", "D4", "V", "N"]:
    with io.open(f"agentsec/results/{cfg}.json", encoding="utf-8") as f:
        d = json.load(f)
    print(f"===== {cfg} =====")
    for r in d["results"]:
        tag = "恶意" if r["malicious"] else "良性"
        print(f"  {r['scenario']} {r['attack']} [{tag}] tool={str(r['tool'])[:38]!r:42} executed={r['executed']} | {r['reason'][:40]}")
    print()
