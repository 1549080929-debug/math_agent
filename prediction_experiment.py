"""对抗性预测实验（三阶段）：

阶段1 预测表：让 LLM 生成 5 道"它预测 baseline 会翻车"的题，
             并写明每题的预测失败模式、翻车根因、系统凭什么能对。
阶段2 实跑：  baseline（直接单次求解） vs 系统（拆解-验证-纠错）跑同样的题。
阶段3 复盘：  把实际结果喂回 LLM，对照预测表逐条分析"预测对了没有，为什么"。

输出：
    data/prediction_set.json        预测表（阶段1）
    data/prediction_experiment_results.json  实际结果（阶段2）
    data/prediction_review.md       复盘报告（阶段3）
"""

import json
import os

from baseline import solve_direct
from llm_client import chat, chat_json, parse_json
from main import run_problem

OUT_DIR = "data"
PREDICTION_FILE = os.path.join(OUT_DIR, "prediction_set.json")
RESULT_FILE = os.path.join(OUT_DIR, "prediction_experiment_results.json")
REVIEW_FILE = os.path.join(OUT_DIR, "prediction_review.md")

GENERATE_PROMPT = """你是"对抗性出题专家"。生成 5 道**一元二次函数综合题**（纯代数，无几何图形、无实际应用题背景），要求：
**直接让 LLM 单次求解（无验证、无回溯）大概率会翻车，但经过"拆解→子任务→SymPy验证→反馈纠错"流程可以稳对**的题。

题目形态必须限定在以下可被 SymPy 验证的范围内：
- 解方程求根（含二次根式解，如 x=(3+√5)/2，或需要化简的根式）
- 含参二次函数在区间上的最值/参数求值（需要分类讨论、需要检查参数范围）
- 二次函数与直线交点 / 判别式不等式（答案是不等式区间）
- 分数系数、需要细心代数运算的题

每题输出 JSON 字段：
{
  "id": 1,
  "question": "题目（中文，纯代数表达，不要几何图形）",
  "standard_answer": "标准答案（必须唯一且正确）",
  "predicted_failure_mode": "预测 baseline（直接单次求解的 LLM）具体在哪一步出错，必须非常具体。示例：'会在化简 √(8+4√3) 时写成 2√2+√3'、'会漏掉 a>2 的分类讨论'、'会把判别式小于0写成大于0'、'解方程时两边除以x导致丢根'、'算端点值 f(1) 时算错'",
  "why_baseline_fails": "翻车根因（从'记忆解题、无验证、无回溯'角度解释）",
  "why_system_wins": "系统凭什么能对（指出具体哪个环节兜住：哪个子任务被 SymPy 验证、哪次反馈纠错会修正、哪次回溯会重拆）"
}

要求：
1. 5 道题的失败模式尽量多样化：算术错误、漏分类讨论、忘检查定义域/范围、根式化简、不等式方向、丢根等各覆盖一种。
2. 每题标准答案唯一、可验证。
3. 难度可以高于基础测试题，但必须在上述形态范围内。

输出 JSON：{"problems": [...]}"""

REVIEW_SYSTEM_PROMPT = """你是实验复盘员。下面是"对抗性预测实验"的完整记录：
我们事先对每题预测了 baseline（直接单次求解的 LLM）会怎么翻车、系统（拆解-验证-纠错）凭什么能对；
然后实际跑了 baseline 和系统。

对每题逐条复盘：
1. prediction_was_correct：预测对了没有？（完全正确 / 部分正确 / 没对）
2. baseline_actual：baseline 实际怎么表现的？如果错了，具体错在哪一步？
3. system_actual：系统实际表现如何？子任务验证状态是什么（PASS/FAIL/UNSURE）？最终答案对不对？
4. analysis：为什么预测对/错？（如果 baseline 没按预测的方式翻车，实际怎么翻的？如果系统没兜住，为什么？）
5. lesson：这次实验教会我们什么？对改进系统有什么启示？

输出 JSON：{"reviews": [{"id": 1, "prediction_was_correct": "...", "baseline_actual": "...", "system_actual": "...", "analysis": "...", "lesson": "..."}]}"""


def truncate(text, n=700):
    text = text or ""
    return text if len(text) <= n else text[:n] + "……[截断]"


def generate_prediction_set():
    print("\n[阶段1/3] 生成对抗性题目 + 预测表 ...")
    data = chat_json([
        {"role": "system", "content": GENERATE_PROMPT},
        {"role": "user", "content": "请生成 5 道题和对应的预测表。"},
    ], temperature=0.4, max_tokens=4000)
    problems = data.get("problems", data if isinstance(data, list) else [])
    with open(PREDICTION_FILE, "w", encoding="utf-8") as f:
        json.dump({"problems": problems}, f, ensure_ascii=False, indent=2)
    print(f"  已保存预测表：{PREDICTION_FILE}（{len(problems)} 题）")
    return problems


def load_or_generate():
    if os.path.exists(PREDICTION_FILE):
        with open(PREDICTION_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("problems"):
            print(f"  复用已有预测表：{PREDICTION_FILE}（删除该文件可重新生成）")
            return data["problems"]
    return generate_prediction_set()


def main():
    problems = load_or_generate()

    print("\n[阶段2/3] 实跑 baseline vs 系统 ...")
    actuals = []
    for p in problems:
        q = p["question"]
        print("\n" + "=" * 60)
        print(f"题 {p.get('id')}：{q}")
        print(f"  预测失败模式：{p.get('predicted_failure_mode', '')}")
        print("=" * 60)

        # ---- baseline ----
        try:
            base_out = solve_direct(q)
        except Exception as e:
            base_out = f"[baseline 异常] {e}"
        print(f"  [baseline] {truncate(base_out, 250)}")

        # ---- 系统 ----
        try:
            sys_res = run_problem(q, standard_answer=p.get("standard_answer"), verbose=False)
            if sys_res.get("ok"):
                sys_out = sys_res.get("answer", "")
            else:
                sys_out = "[系统未能解决，见 logs/run_log.jsonl]"
        except Exception as e:
            sys_res = {"ok": False, "results": []}
            sys_out = f"[系统异常] {e}"
        statuses = [r["verify"].status for r in sys_res.get("results", [])]
        print(f"  [系统] ok={sys_res.get('ok')} 子任务验证={statuses}")

        actuals.append({
            "id": p.get("id"),
            "question": q,
            "standard_answer": p.get("standard_answer", ""),
            "predicted_failure_mode": p.get("predicted_failure_mode", ""),
            "why_baseline_fails": p.get("why_baseline_fails", ""),
            "why_system_wins": p.get("why_system_wins", ""),
            "baseline_output": truncate(base_out, 800),
            "system_output": truncate(sys_out, 800),
            "system_ok": sys_res.get("ok", False),
            "system_verify_statuses": statuses,
        })

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump({"problems": actuals}, f, ensure_ascii=False, indent=2)
    print(f"\n  已保存实际结果：{RESULT_FILE}")

    print("\n[阶段3/3] 对照预测表复盘 ...")
    payload = json.dumps(actuals, ensure_ascii=False, indent=2)
    review_text = chat([
        {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
        {"role": "user", "content": f"以下是实验记录：\n{payload}\n\n请逐条复盘并输出 JSON。"},
    ], temperature=0.3, max_tokens=4000)

    try:
        review_data = parse_json(review_text)
    except Exception:
        review_data = {"raw": review_text}

    lines = [
        "# 对抗性预测实验复盘报告", "",
        "> 流程：生成预测表 → 实跑 baseline vs 系统 → 对照预测逐条复盘", "",
    ]
    if "raw" in review_data:
        lines.append(review_text)
    else:
        for r in review_data.get("reviews", []):
            lines += [
                f"## 题 {r.get('id')}", "",
                f"- **预测判定**：{r.get('prediction_was_correct', '')}", "",
                f"- **baseline 实际**：{r.get('baseline_actual', '')}", "",
                f"- **系统实际**：{r.get('system_actual', '')}", "",
                f"- **分析**：{r.get('analysis', '')}", "",
                f"- **教训**：{r.get('lesson', '')}", "",
            ]
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  已保存复盘报告：{REVIEW_FILE}")


if __name__ == "__main__":
    main()
