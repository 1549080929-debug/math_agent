"""P3 实验：类型信息对代码生成正确性的影响（HumanEval 子集）。

条件（对照 docs/08 P3）：
  A 裸生成 —— 剥离类型标注的签名（无类型信息）
  B 带类型 —— HumanEval 原题面（含类型标注）
  C 带类型 + mypy 类型检查反馈（1 轮修复）——L3 锚（类型检查器）入环

指标：pass@1（生成代码通过 HumanEval 测试）；C 额外记录 mypy 报错数。
样本：前 N 题（默认 12），deepseek-chat，温度 0.2 —— pilot 规模，诚实标注。
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from llm_client import chat  # noqa: E402

TEMPERATURE = 0.2

SYS_PROMPT = ("你是一个 Python 程序员。只输出完整的函数定义代码（含 def 行），"
              "不要任何解释文字，不要 Markdown 代码块标记。")


def load_problems():
    lines = open(os.path.join(HERE, "HumanEval.jsonl"), encoding="utf-8").read().splitlines()
    return [json.loads(l) for l in lines]


def split_top_level(s):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def strip_type_hints(prompt):
    """剥离 def 行的类型标注（保留 def 行前的导入与行后的 docstring）；多行签名返回 (prompt, False)。"""
    m = re.search(r'^def\s+\w+\s*\(([^)]*)\)\s*(->[^:]*)?:', prompt, re.M)
    if not m:
        return prompt, False
    params = m.group(1)
    parts = []
    for part in split_top_level(params):
        part = part.strip()
        if ":" in part:
            name, rest = part.split(":", 1)
            rest = rest.strip()
            if "=" in rest:
                _, default = rest.split("=", 1)
                parts.append(f"{name.strip()}={default.strip()}")
            else:
                parts.append(name.strip())
        else:
            parts.append(part)
    fname = re.search(r'^def\s+(\w+)', prompt[m.start():], re.M).group(1)
    new_def = "def " + fname + "(" + ", ".join(parts) + "):"
    return prompt[:m.start()] + new_def + prompt[m.end():], True


def extract_code(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:] if lines and lines[0].startswith("```") else lines
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def generate(prompt, feedback=None):
    msgs = [{"role": "system", "content": SYS_PROMPT}]
    if feedback:
        msgs.append({"role": "user",
                     "content": prompt + "\n\n【类型检查反馈】你的上一次实现存在以下类型错误，请修正后重新输出完整代码：\n" + feedback})
    else:
        msgs.append({"role": "user", "content": prompt + "\n\n请完成这个函数实现。"})
    for attempt in range(3):
        try:
            return extract_code(chat(msgs, temperature=TEMPERATURE, max_tokens=1200))
        except Exception as e:
            print(f"  [generate retry {attempt}] {e}")
            time.sleep(2)
    return ""


def header_of(prompt):
    """def 行之前的内容（导入区）。生成代码假设该上下文存在。"""
    m = re.search(r'^def\s+\w+', prompt, re.M)
    return prompt[:m.start()] if m else ""


def mypy_check(code, header=""):
    """返回 mypy 错误列表（前 15 条）。"""
    f = os.path.join(HERE, "_tmp_check.py")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(header + "\n" + code)
    try:
        r = subprocess.run([sys.executable, "-m", "mypy", "--ignore-missing-imports", "--no-error-summary", f],
                           capture_output=True, text=True, timeout=60)
        errs = [ln for ln in r.stdout.splitlines() if "error:" in ln]
        return errs[:15]
    except Exception as e:
        return [f"mypy 执行失败: {e}"]
    finally:
        try:
            os.remove(f)
        except OSError:
            pass


def run_tests(code, test_str, header=""):
    full = header + "\n" + code + "\n\n" + test_str
    try:
        r = subprocess.run([sys.executable, "-c", full], capture_output=True, text=True, timeout=20)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def main():
    """两阶段协议（框架方法论：先测价值窗口，再在窗口内比较）：
      scan N   —— 阶段 1：条件 A 扫 N 题，找失败题（窗口）
      window   —— 阶段 2：仅在窗口题上跑 B/C 比较
    """
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    probs = load_problems()

    if mode == "scan":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        scan = []
        for p in probs[start:start + n]:
            tid = p["task_id"]
            prompt = p["prompt"]
            header = header_of(prompt)
            stripped, ok = strip_type_hints(prompt)
            if not ok:
                continue
            code_a = generate(stripped)
            pass_a = run_tests(code_a, p["test"], header) if code_a else False
            scan.append({"task": tid, "A_pass": pass_a, "code_A": code_a,
                         "prompt": prompt, "header": header, "test": p["test"]})
            print(f"{tid}: A={'✓' if pass_a else '✗'}")
        fails = [r for r in scan if not r["A_pass"]]
        # 合并进既有扫描文件
        f_scan = os.path.join(HERE, "p3_scan.json")
        prev = json.load(open(f_scan, encoding="utf-8")) if os.path.exists(f_scan) else []
        merged = {r["task"]: r for r in prev}
        for r in scan:
            merged[r["task"]] = r
        all_rows = list(merged.values())
        with open(f_scan, "w", encoding="utf-8") as fh:
            json.dump(all_rows, fh, ensure_ascii=False, indent=1)
        all_fails = [r for r in all_rows if not r["A_pass"]]
        print(f"\n本轮 {start}–{start+len(scan)-1}：A 通过 {len(scan)-len(fails)}，失败 {len(fails)}")
        print(f"累计扫描 {len(all_rows)} 题：失败 {len(all_fails)}（价值窗口）")
        print("窗口题:", [r["task"] for r in all_fails])
        return

    if mode == "window":
        scan = json.load(open(os.path.join(HERE, "p3_scan.json"), encoding="utf-8"))
        fails = [r for r in scan if not r["A_pass"]]
        rows = []
        for r in fails:
            tid = r["task"]
            prompt = r["prompt"]
            header = r["header"]
            test_str = r["test"]
            code_b = generate(prompt)
            pass_b = run_tests(code_b, test_str, header) if code_b else False
            errs = mypy_check(code_b, header) if code_b else []
            if errs and not pass_b:
                code_c = generate(prompt, feedback="\n".join(errs))
                pass_c = run_tests(code_c, test_str, header) if code_c else False
            else:
                code_c, pass_c = code_b, pass_b
            rows.append({"task": tid, "A_pass": False, "B_pass": pass_b, "C_pass": pass_c,
                         "mypy_errors_before": len(errs), "C_repaired": bool(errs and not pass_b),
                         "code_A": r["code_A"], "code_B": code_b, "code_C": code_c})
            print(f"{tid}: B={'✓' if pass_b else '✗'} C={'✓' if pass_c else '✗'} mypy_errs={len(errs)}")
        n = len(rows)
        b = sum(x["B_pass"] for x in rows)
        c = sum(x["C_pass"] for x in rows)
        print("\n" + "=" * 50)
        print(f"窗口内 {n} 题（A 全部失败）")
        print(f"B 带类型:      {b}/{n} = {b/n:.0%}  （相对 A 的提升量）")
        print(f"C 类型检查反馈: {c}/{n} = {c/n:.0%}  （相对 B 的增量）")
        with open(os.path.join(HERE, "p3_results.json"), "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
        print("结果已存: chapter4/p3_results.json")
        return

    if mode == "hard":
        from hard_problems import PROBLEMS
        rows = []
        for p in PROBLEMS:
            tid = p["id"]
            prompt = p["prompt"]
            header = header_of(prompt)
            stripped, ok = strip_type_hints(prompt)
            test_str = p["test"]
            code_a = generate(stripped if ok else prompt)
            pass_a = run_tests(code_a, test_str, header) if code_a else False
            code_b = generate(prompt)
            pass_b = run_tests(code_b, test_str, header) if code_b else False
            errs = mypy_check(code_b, header) if code_b else []
            if errs and not pass_b:
                code_c = generate(prompt, feedback="\n".join(errs))
                pass_c = run_tests(code_c, test_str, header) if code_c else False
            else:
                code_c, pass_c = code_b, pass_b
            rows.append({"task": tid, "A_pass": pass_a, "B_pass": pass_b, "C_pass": pass_c,
                         "mypy_errors_before": len(errs), "C_repaired": bool(errs and not pass_b),
                         "code_A": code_a, "code_B": code_b, "code_C": code_c})
            print(f"{tid}: A={'✓' if pass_a else '✗'} B={'✓' if pass_b else '✗'} "
                  f"C={'✓' if pass_c else '✗'} mypy_errs={len(errs)}")
        n = len(rows)
        a = sum(r["A_pass"] for r in rows)
        b = sum(r["B_pass"] for r in rows)
        c = sum(r["C_pass"] for r in rows)
        print("\n" + "=" * 50)
        print(f"手写难题 {n} 题（deepseek-chat, T={TEMPERATURE}）")
        print(f"A 裸生成:        {a}/{n} = {a/n:.0%}")
        print(f"B 带类型:        {b}/{n} = {b/n:.0%}")
        print(f"C 类型检查反馈:   {c}/{n} = {c/n:.0%}")
        with open(os.path.join(HERE, "p3_hard_results.json"), "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
        print("结果已存: chapter4/p3_hard_results.json")
        return

    print("用法: p3_experiment.py scan <N> [start] | window | hard")


if __name__ == "__main__":
    main()
