"""主流程：入口分类 → 拆解 → 自查 → 逐个子任务(求解+验证+反馈) → 回溯 → 组合 → 诚实失败出口

架构一句话：LLM 只做"翻译"（拆解/求解/组装），SymPy 做"裁判"（验证/纠错），
所有数学事实必须经过确定性验证后才被允许进入下一步。
"""

import argparse
import datetime
import json
import sys

from config import MAX_REDECOMPOSE, MAX_VERIFY_RETRIES
from combiner import combine
from decomposer import classify, decompose, self_check
from final_check_deriver import derive_final_check
from solver import fix_subtask, solve_subtask
from verifier import VerifyResult, run_verify

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def topological_order(subtasks):
    """按依赖关系给子任务排序；同一层可执行的子任务按权重从高到低（weight 的真实用途）。"""
    done = set()
    order = []
    remaining = list(subtasks)
    while remaining:
        ready = [s for s in remaining if all(d in done for d in (s.get("depends_on") or []))]
        if not ready:
            order.extend(remaining)
            break
        ready.sort(key=lambda s: s.get("weight", 0), reverse=True)
        s = ready[0]
        order.append(s)
        done.add(s.get("id"))
        remaining.remove(s)
    return order


def _fill_answer(params, answer):
    """把 verify.params 里所有 "<answer>" 替换为子任务实际答案。"""
    if isinstance(params, dict):
        return {k: _fill_answer(v, answer) for k, v in params.items()}
    if isinstance(params, list):
        return [_fill_answer(x, answer) for x in params]
    if isinstance(params, str) and params == "<answer>":
        return answer
    return params


def try_verify(vtype, vparams, answer):
    """根据验证类型分发，把 LLM 答案注入验证参数。"""
    p = _fill_answer(vparams or {}, answer)
    if vtype == "root":
        return run_verify("root", equation=p.get("equation"), root=answer,
                          var_name=p.get("var_name", "x"))
    if vtype == "extreme":
        return run_verify("extreme", expr=p.get("expr"), point=answer,
                          var_name=p.get("var_name", "x"))
    if vtype == "interval_extreme":
        return run_verify("interval_extreme", expr=p.get("expr"),
                          var_name=p.get("var_name", "x"),
                          interval=p.get("interval", ["0", "1"]),
                          claimed=p.get("claimed"),
                          which=p.get("which", "min"),
                          subs=p.get("subs"))
    if vtype == "equality":
        return run_verify("equality", expr1=p.get("expr1"), expr2=answer)
    if vtype == "satisfies":
        return run_verify("satisfies", condition=p.get("condition"), value=answer,
                          var_name=p.get("var_name", "x"))
    if vtype == "inequality":
        return run_verify("inequality", condition=p.get("condition"), claimed=answer,
                          var_name=p.get("var_name", "x"))
    return VerifyResult("UNSURE", f"未知验证类型：{vtype}")


def log_case(entry):
    """把每次运行记录追加到 logs/run_log.jsonl（经验库 P8 的地基）。"""
    import os
    os.makedirs("logs", exist_ok=True)
    with open("logs/run_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def run_problem(question, standard_answer=None, verbose=True):
    if verbose:
        print("\n" + "=" * 64)
        print("题目：", question)
        print("=" * 64)

    # 第1步：入口分类（初段判断）
    if verbose:
        print("\n[1/6] 入口分类（初段判断）...")
    cls = classify(question)
    if verbose:
        print("  分类：", json.dumps(cls, ensure_ascii=False))

    subtasks, results, ok = [], [], False
    final_check = None

    # 终局验证规格：规则从题面自动派生（确定性、不依赖 LLM），派生失败才用 LLM 声明的兜底
    rule_fc, rule_reason = derive_final_check(question)
    if verbose and rule_fc:
        print("  [规则派生] 终局验证规格：", json.dumps(rule_fc["params"], ensure_ascii=False)[:200])

    for rd in range(MAX_REDECOMPOSE + 1):
        # 第2步：拆解
        if verbose:
            print(f"\n[2/6] 拆解子任务（第 {rd + 1} 轮）...")
        subtasks, final_check = decompose(question, cls)
        if verbose:
            print(f"  拆出 {len(subtasks)} 个子任务"
                  + ("，含终局验证 final_check" if final_check else ""))

        # 第3步：拆解自查
        if verbose:
            print("[3/6] 拆解自查（质检）...")
        subtasks, issues = self_check(question, subtasks)
        if verbose and issues:
            print("  自查意见：", "；".join(issues)[:200])

        # 第4步：逐个求解 + 验证 + 反馈
        order = topological_order(subtasks)
        context = {}       # 已验证结果共享区（上下文传递）
        results = []       # 每个子任务的最终结果
        trace = []         # 完整过程痕迹：拆解 + 每次求解/验证/重试（审计要求留痕）
        failed_here = False

        trace.append({"stage": "decompose", "round": rd,
                      "subtasks": subtasks, "constraints": cls.get("constraints", {}),
                      "final_check": final_check})

        for idx, sub in enumerate(order, 1):
            if verbose:
                print(f"\n[4/6] 子任务 {idx}/{len(order)}：{sub['task'][:70]}")

            constraints = cls.get("constraints")

            # 首次求解（异常转为 FAIL，不崩溃——LLM JSON 损坏等）
            try:
                res = solve_subtask(question, sub, context, constraints=constraints)
                verify = sub.get("verify") or {}
                vtype = verify.get("type", "equality")
                vparams = verify.get("params") or {}
                vr = try_verify(vtype, vparams, res.get("answer", ""))
            except Exception as e:
                res = {"answer": ""}
                verify = sub.get("verify") or {}
                vtype = verify.get("type", "equality")
                vparams = verify.get("params") or {}
                vr = VerifyResult("FAIL", f"求解/验证异常：{e}")

            # 类型核查（类型系统）：声明的答案类型 vs 实际类型
            declared_type = sub.get("type")
            tvr = VerifyResult("UNSURE", "未声明类型（跳过）")
            if declared_type:
                tvr = run_verify("answer_type", declared_type=declared_type,
                                 answer=res.get("answer", ""),
                                 var_name=vparams.get("var_name", "x"))
            if verbose:
                print(f"  首轮验证：{vr.status}  | {vr.message[:100]}")
                if declared_type:
                    print(f"  类型核查：{tvr.status}（声明 {declared_type}）| {tvr.message[:80]}")
            trace.append({"stage": "solve", "subtask": sub["task"], "attempt": 0,
                          "status": vr.status, "type_status": tvr.status,
                          "verify_message": vr.message, "answer": res.get("answer", "")})

            # 反馈纠错循环（补丁 P2 + 类型不符也触发纠错）
            retry = 0
            while (vr.status == "FAIL" or tvr.status == "FAIL") and retry < MAX_VERIFY_RETRIES:
                retry += 1
                if verbose:
                    print(f"  → 反馈纠错（第 {retry}/{MAX_VERIFY_RETRIES} 次）...")
                hints = []
                if vr.status == "FAIL":
                    hints.append(vr.message)
                if tvr.status == "FAIL":
                    hints.append(f"类型核查失败：声明 {declared_type}")
                try:
                    res = fix_subtask(question, sub, context, res, "；".join(hints), retry,
                                      constraints=constraints)
                    vr = try_verify(vtype, vparams, res.get("answer", ""))
                except Exception as e:
                    res = {"answer": ""}
                    vr = VerifyResult("FAIL", f"修正异常：{e}")
                if declared_type:
                    tvr = run_verify("answer_type", declared_type=declared_type,
                                     answer=res.get("answer", ""),
                                     var_name=vparams.get("var_name", "x"))
                if verbose:
                    print(f"  验证：{vr.status}  | {vr.message[:100]}")
                    if declared_type:
                        print(f"  类型核查：{tvr.status} | {tvr.message[:80]}")
                trace.append({"stage": "solve", "subtask": sub["task"], "attempt": retry,
                              "status": vr.status, "type_status": tvr.status,
                              "verify_message": vr.message, "answer": res.get("answer", "")})

            if vr.status == "FAIL" or tvr.status == "FAIL":
                if verbose:
                    print(f"  ✗ 子任务失败（重试 {MAX_VERIFY_RETRIES} 次仍错）→ 触发回溯重拆")
                failed_here = True
                break
            if vr.status == "UNSURE":
                if verbose:
                    print("  ⚠ 验证器弃权（UNSURE）→ 结果标记待人工确认，继续流程")

            # 结果存入上下文，供后续子任务使用（上下文传递）
            context[f"sub{idx}"] = res.get("answer", "")
            results.append({"subtask": sub, "result": res, "verify": vr})

        if not failed_here:
            ok = True
            break
        if rd < MAX_REDECOMPOSE and verbose:
            print("\n↩ 回溯：携带上次失败信息，重新拆解整题...")

    if not ok:
        # 诚实失败出口
        last = results[-1] if results else None
        if verbose:
            print("\n" + "-" * 64)
            print("✗ 未能解决该题（诚实失败，不做死循环）。")
            if last:
                print("  卡在子任务：", last["subtask"]["task"])
                print("  验证器信息：", last["verify"].message)
            print("  该失败案例已记录，可用于后续改进（经验库 P8）。")
        log_case({"time": datetime.datetime.now().isoformat(), "question": question,
                  "ok": False, "stage": "solve", "cls": cls, "trace": trace})
        return {"ok": False, "stage": "solve", "results": results, "trace": trace}

    # 终局验证规格决策：规则派生 > LLM 声明（信任递归修正：优先不依赖 LLM 的来源）
    fc_source = "none"
    if rule_fc:
        final_check = rule_fc
        fc_source = "rule"
    elif final_check:
        fc_source = "llm"
    if verbose:
        print(f"\n[5/6] 终局验证规格来源：{fc_source}"
              + (f"（规则派生失败：{rule_reason}）" if fc_source != "rule" else ""))

    # 第5步：组合（只用已验证结果，禁止重算）
    if verbose:
        print("组合最终解答（模板组装，禁止重算）...")
    final = combine(question, results)
    final_answer = final.get("answer", "")
    final_text = final.get("text", "")
    if verbose:
        print("-" * 64)
        print("最终解答：\n")
        print(final_text)
        if final_answer:
            print(f"\n[结构化答案] {final_answer}")
        print("-" * 64)

    # 第6步：终局验证（审计修正第 2 波——抓"推理对、终局错"）
    final_vr = VerifyResult("UNSURE", "无 final_check，跳过终局验证")
    if final_check and final_check.get("type") == "final_parameter_set" and final_answer:
        fp = final_check.get("params") or {}
        final_vr = run_verify("final_parameter_set", claimed=final_answer,
                              expr=fp.get("expr"), var_name=fp.get("var_name", "x"),
                              param_name=fp.get("param_name", "a"),
                              interval=fp.get("interval"), conditions=fp.get("conditions"))
        if verbose:
            print(f"\n[6/6] 终局验证：{final_vr.status} | {final_vr.message[:140]}")
        # 终局修正循环（最多 2 次）
        for fa in range(2):
            if final_vr.status != "FAIL":
                break
            if verbose:
                print(f"  → 终局修正（第 {fa + 1}/2 次）...")
            hint = (f"{final_vr.message}。请修正 answer 字段：收缩集合，使集合内每个点都满足条件；"
                    f"answer 只输出规范集合（如 '0<=a<=1'），禁止任何解释文字。")
            final = combine(question, results, retry_hint=hint)
            final_answer = final.get("answer", "")
            final_text = final.get("text", "")
            final_vr = run_verify("final_parameter_set", claimed=final_answer,
                                  expr=fp.get("expr"), var_name=fp.get("var_name", "x"),
                                  param_name=fp.get("param_name", "a"),
                                  interval=fp.get("interval"), conditions=fp.get("conditions"))
            if verbose:
                print(f"  终局验证：{final_vr.status} | {final_vr.message[:140]}")

    # 终局 FAIL 未修正 → 诚实失败标记
    answer_verified = final_vr.status == "PASS"
    if final_vr.status == "FAIL":
        if verbose:
            print(f"\n✗ 终局验证失败且未能修正：{final_vr.message[:120]}")
            print("  最终答案不可信（诚实失败：不把未通过终局验证的答案当作结果）。")

    # 最终核对（若提供标准答案）
    if standard_answer:
        if verbose:
            print("  标准答案：", standard_answer, "（人工比对）")

    # 验证覆盖统计（审计修正：ok 只表示"流程走完"，不表示"答案已全部验证"）
    status_counts = {"PASS": 0, "FAIL": 0, "UNSURE": 0}
    for r in results:
        status_counts[r["verify"].status] += 1
    all_verified = len(results) > 0 and status_counts["PASS"] == len(results)

    log_case({"time": datetime.datetime.now().isoformat(), "question": question,
              "ok": True, "cls": cls,
              "status_counts": status_counts, "all_subtasks_verified": all_verified,
              "final_verify": final_vr.status, "final_answer": final_answer,
              "results": [{"task": r["subtask"]["task"], "status": r["verify"].status}
                          for r in results],
              "trace": trace})
    return {"ok": True, "answer": final_text, "final_answer": final_answer,
            "final_verify": final_vr.status, "answer_verified": answer_verified,
            "has_final_check": bool(final_check and final_check.get("type") == "final_parameter_set"),
            "final_check_source": fc_source,
            "context": context, "results": results,
            "trace": trace, "status_counts": status_counts,
            "all_subtasks_verified": all_verified}


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="数学推理代理：LLM 拆解 + SymPy 验证 + 反馈纠错")
    parser.add_argument("--problem", "-p", help="直接输入一道题")
    parser.add_argument("--file", "-f", default="data/problems.json", help="批量跑 data/problems.json")
    args = parser.parse_args()

    if args.problem:
        run_problem(args.problem)

    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                problems = json.load(f)
        except FileNotFoundError:
            print(f"找不到题目文件：{args.file}")
            sys.exit(1)
        ok_count = 0
        for i, p in enumerate(problems, 1):
            r = run_problem(p["question"], p.get("standard_answer"))
            if r["ok"]:
                ok_count += 1
            print(f"\n>>> 进度：{i}/{len(problems)}，当前正确 {ok_count} 题")
        print(f"\n=== 汇总：{ok_count}/{len(problems)} 题成功 ===")

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"\n[配置错误] {e}")
        print("请在 config.py 中填写你的 DeepSeek API Key，或设置环境变量 DEEPSEEK_API_KEY。")
        sys.exit(1)
