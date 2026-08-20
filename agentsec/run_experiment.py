"""部署价值实验：VAL 选型(V=D3+D4) vs 直觉选型(N=D1+D2) vs 单防御。

用法：
  python agentsec/run_experiment.py --dry        # harness 验证（预定调用，无 LLM）
  python agentsec/run_experiment.py --full       # 真跑（DeepSeek，temperature 0.2）
输出：控制台汇总表 + results/<config>.json
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agent import Agent, SYSTEM_BASE, run_defense_chain
from attacks import attack_direct, attack_fake_confirm, attack_paraphrase
from defenses import D1_SYSTEM_PROMPT, StubExecutor

SCEN = os.path.join(HERE, "scenarios.json")

CONFIGS = {
    "D1": (["D1"], "单防御：系统提示加固(L0)"),
    "D2": (["D2"], "单防御：关键词过滤(L1)"),
    "D3": (["D3"], "单防御：确认门禁(L1/L2)"),
    "D4": (["D4"], "单防御：参数沙箱(L3风味)"),
    "V":  (["D3", "D4"], "VAL 选型：确认门禁+参数沙箱"),
    "N":  (["D1", "D2"], "直觉选型：提示加固+关键词过滤"),
}


def get_variants(sc):
    """恶意场景 3 变体（A1/A2/A3）；良性 1 变体。"""
    if sc["malicious"]:
        return [("A1", attack_direct(sc["memory_text"])),
                ("A2", attack_paraphrase(sc["memory_text"])),
                ("A3", attack_fake_confirm(sc["memory_text"]))]
    return [("B", sc["memory_text"])]


def run_config(name, enabled, label, scenarios, dry_run):
    results = []
    for sc in scenarios["scenarios"]:
        for vname, mem in get_variants(sc):
            system = D1_SYSTEM_PROMPT if "D1" in enabled else SYSTEM_BASE
            agent = Agent(system_prompt=system, dry_run=dry_run)
            proposal = agent.propose(
                sc["user_task"], mem, sc["memory_source"],
                {"tool": sc["target_tool"], "args": sc["target_args"]})
            executor = StubExecutor()
            executed, reasons = run_defense_chain(
                proposal, mem, json.dumps(proposal, ensure_ascii=False),
                sc["confirmation_recorded"], sc["authorized"],
                scenarios["tools"], enabled, executor)
            results.append({
                "scenario": sc["id"], "attack": vname, "malicious": sc["malicious"],
                "tool": proposal.get("tool"), "executed": executed,
                "reason": reasons[-1] if reasons else "",
            })
    return results


def summarize(results):
    mal = [r for r in results if r["malicious"]]
    ben = [r for r in results if not r["malicious"]]
    asr = sum(r["executed"] for r in mal) / len(mal) if mal else None
    bsucc = sum(r["executed"] for r in ben) / len(ben) if ben else None
    return asr, bsucc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="harness 验证模式（预定调用）")
    ap.add_argument("--full", action="store_true", help="真跑模式（DeepSeek）")
    args = ap.parse_args()
    dry_run = not args.full

    with io.open(SCEN, encoding="utf-8") as f:
        scenarios = json.load(f)

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    print(f"{'配置':<28}{'ASR(恶意)':<12}{'良性成功':<12}{'说明'}")
    print("-" * 78)
    all_out = {}
    for name, (enabled, label) in CONFIGS.items():
        results = run_config(name, enabled, label, scenarios, dry_run)
        asr, bsucc = summarize(results)
        all_out[name] = results
        print(f"{name + ' ' + ('(dry)' if dry_run else ''):<28}{asr:<12.3f}{bsucc:<12.3f}{label}")
        with io.open(os.path.join(HERE, "results", f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump({"config": name, "dry_run": dry_run, "results": results},
                      f, ensure_ascii=False, indent=2)

    # 预期对照（H1/H2）
    print("\n预期（H1）：V 栈 ASR < N 栈 ASR 且良性 V >= N")
    if dry_run:
        print("当前为 dry-run（预定调用），仅供 harness 验证；真跑请用 --full")


if __name__ == "__main__":
    main()
