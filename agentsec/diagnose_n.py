"""诊断：N 栈自适应攻击为何 0 突破——看每轮的提议形态。"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from adaptive_attack import CONFIGS, adaptive_attack
from defenses import HIGH_RISK


def main():
    with io.open(os.path.join(HERE, "scenarios.json"), encoding="utf-8") as f:
        scen = json.load(f)
    enabled, sys_prompt = CONFIGS["N"]
    for sc in scen["scenarios"]:
        if sc["malicious"] and sc["id"] in ("S01", "S06", "S09", "S18", "S22"):
            ok, rnds, trail = adaptive_attack(sc, enabled, sys_prompt, scen["tools"], 3, verbose=False)
            print(f"=== {sc['id']}: success={ok} rounds={rnds} ===")
            for t in trail:
                tool = t["proposal"].get("tool", "")
                args = t["proposal"].get("args", {})
                if tool in HIGH_RISK and args:
                    tag = "高危+args"
                elif tool in HIGH_RISK:
                    tag = "高危+空args"
                elif tool:
                    tag = "低危/" + tool
                else:
                    tag = "空提议"
                print(f"  r{t['round']}: {tag} | {t['reasons'][-1][:60]}")


if __name__ == "__main__":
    main()
