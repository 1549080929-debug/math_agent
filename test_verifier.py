"""离线测试验证器（不需要 API Key）——先确认"裁判"本身是靠谱的。"""

from verifier import run_verify

CASES = [
    # (验证类型, 参数, 答案, 期望状态)
    ("root",  {"equation": "x**2 - 5*x + 6", "var_name": "x"}, "2", "PASS"),
    ("root",  {"equation": "x**2 - 5*x + 6", "var_name": "x"}, "5", "FAIL"),
    ("root",  {"equation": "x**2 - 3", "var_name": "x"}, "1.73205080756888", "PASS"),
    ("extreme", {"expr": "x**2 - 4*x + 7", "var_name": "x"}, "2", "PASS"),
    ("extreme", {"expr": "x**2 - 4*x + 7", "var_name": "x"}, "1", "FAIL"),
    ("interval_extreme", {"expr": "x**2 - 4*x + 7", "var_name": "x",
                          "interval": ["1", "4"], "which": "min", "claimed": "<answer>"}, "3", "PASS"),
    ("interval_extreme", {"expr": "x**2 - 4*x + 7", "var_name": "x",
                          "interval": ["1", "4"], "which": "min", "claimed": "<answer>"}, "5", "FAIL"),
    ("interval_extreme", {"expr": "x**2 - 2*a*x + 1", "var_name": "x",
                          "interval": ["0", "2"], "which": "min", "claimed": "-1",
                          "subs": {"a": "<answer>"}}, "sqrt(2)", "PASS"),
    ("interval_extreme", {"expr": "x**2 - 2*a*x + 1", "var_name": "x",
                          "interval": ["0", "2"], "which": "min", "claimed": "-1",
                          "subs": {"a": "<answer>"}}, "3", "FAIL"),
    ("equality", {"expr1": "sin(x)**2"}, "1 - cos(x)**2", "PASS"),
    ("equality", {"expr1": "sin(x)**2"}, "cos(x)**2", "FAIL"),
    ("equality", {"expr1": "2*x - 4"}, "2x-4", "PASS"),          # 缺乘号规范化
    ("equality", {"expr1": "x**2 - 2*m*x + m**2 - 1 - (2*x - 3)"}, "x**2 - (2m+2)x + m^2+2 = 0", "PASS"),   # 等式形式
    ("equality", {"expr1": "x**2 - 2*m*x + m**2 - 1 - (2*x - 3)"}, "x**2 - (2m+2)x + (m^2-4) = 0", "FAIL"),  # 常数项错误
    ("root",  {"equation": "x**2 - 4*x + 7", "var_name": "x"}, "2", "FAIL"),
    ("satisfies", {"condition": "x > 0", "var_name": "x"}, "5", "PASS"),
    ("satisfies", {"condition": "x > 0", "var_name": "x"}, "-3", "FAIL"),
    ("satisfies", {"condition": "1 <= x <= 4", "var_name": "x"}, "2", "PASS"),
    ("satisfies", {"condition": "1 <= x <= 4", "var_name": "x"}, "5", "FAIL"),
    ("inequality", {"condition": "8*m - 4 > 0", "var_name": "m"}, "m > 1/2", "PASS"),
    ("inequality", {"condition": "8*m - 4 > 0", "var_name": "m"}, "m < 1 或 m > 2", "FAIL"),
    ("inequality", {"condition": "(k+2)**2 - 4 < 0", "var_name": "k"}, "(-4, 0)", "PASS"),
    ("inequality", {"condition": "(k+2)**2 - 4 < 0", "var_name": "k"}, "k < -4 或 k > 0", "FAIL"),
    ("inequality", {"condition": "a**2 - 2*a <= 0", "var_name": "a"}, "0 <= a <= 2", "PASS"),
    ("inequality", {"condition": "a**2 - 2*a <= 0", "var_name": "a"}, "a = 0 或 a = 2", "FAIL"),
    # 类型系统
    ("answer_type", {"declared_type": "point_set", "var_name": "a"}, "a=1 或 a=2", "PASS"),
    ("answer_type", {"declared_type": "interval", "var_name": "a"}, "a=1 或 a=2", "FAIL"),
    ("answer_type", {"declared_type": "interval", "var_name": "a"}, "0<=a<=2", "PASS"),
    ("answer_type", {"declared_type": "interval", "var_name": "a"}, "[0,2]", "PASS"),
    # 终局验证（抓"推理对、终局错"）
    ("final_parameter_set", {"expr": "x**2 - 2*a*x + 1", "var_name": "x", "param_name": "a",
                             "interval": ["0", "2"],
                             "conditions": [{"which": "min", "op": ">=", "value": "0"},
                                            {"which": "max", "op": "<=", "value": "5"}]},
     "[-1,1]", "FAIL"),
    ("final_parameter_set", {"expr": "x**2 - 2*a*x + 1", "var_name": "x", "param_name": "a",
                             "interval": ["0", "2"],
                             "conditions": [{"which": "min", "op": ">=", "value": "0"},
                                            {"which": "max", "op": "<=", "value": "5"}]},
     "0<=a<=1", "PASS"),
    ("final_parameter_set", {"expr": "x**2 - 2*a*x + 1", "var_name": "x", "param_name": "a",
                             "interval": ["0", "3"],
                             "conditions": [{"which": "diff", "op": "==", "value": "4"}]},
     "a=1 或 a=2", "PASS"),
    ("final_parameter_set", {"expr": "x**2 - 2*a*x + 1", "var_name": "x", "param_name": "a",
                             "interval": ["0", "3"],
                             "conditions": [{"which": "diff", "op": "==", "value": "4"}]},
     "a=1", "UNSURE"),
    ("final_parameter_set", {"expr": "x**2 - 2*a*x + 1", "var_name": "x", "param_name": "a",
                             "interval": ["0", "3"],
                             "conditions": [{"which": "diff", "op": "==", "value": "4"}]},
     "a=-5/6 或 a=3 或 a=13/6", "FAIL"),
    # 解集等价（L3 完备性锚：抓代回验证抓不到的"漏解"与"压缩篡改"）
    ("solution_set", {"expr": "x**2 - 5*x + 6", "var_name": "x"}, "2 或 3", "PASS"),
    ("solution_set", {"expr": "x**2 - 5*x + 6", "var_name": "x"}, "2", "FAIL"),          # 漏解 3
    ("solution_set", {"expr": "x**2 - 3", "var_name": "x"}, "sqrt(3)", "FAIL"),          # 漏 -sqrt(3)
    ("solution_set", {"expr": "x**2 - 3", "var_name": "x"}, "sqrt(3) 或 -sqrt(3)", "PASS"),
    ("solution_set", {"expr": "a**2 - 2*a <= 0", "var_name": "a"}, "0 <= a <= 2", "PASS"),
    ("solution_set", {"expr": "a**2 - 2*a <= 0", "var_name": "a"}, "a = 0 或 a = 2", "FAIL"),  # 压缩篡改（P5）
    ("solution_set", {"expr": "x**2 - 5*x + 6 = 0", "var_name": "x"}, "2 或 3", "PASS"),  # 方程带 =
    ("solution_set", {"expr": "(k+2)**2 - 4 < 0", "var_name": "k"}, "(-4, 0)", "PASS"),   # 与 inequality 同能力
]

passed = 0
for vtype, params, answer, expect in CASES:
    p = dict(params)
    # 把答案注入对应的参数位（与 main.try_verify 的逻辑一致）
    if vtype == "root":
        p["root"] = answer
    elif vtype == "extreme":
        p["point"] = answer
    elif vtype == "interval_extreme":
        if p.get("claimed") == "<answer>":
            p["claimed"] = answer
        if p.get("subs"):
            p["subs"] = {k: (answer if v == "<answer>" else v) for k, v in p["subs"].items()}
    elif vtype == "equality":
        p["expr2"] = answer
    elif vtype == "satisfies":
        p["value"] = answer
    elif vtype == "inequality":
        p["claimed"] = answer
    elif vtype == "solution_set":
        p["claimed"] = answer
    elif vtype == "answer_type":
        p["answer"] = answer
    elif vtype == "final_parameter_set":
        p["claimed"] = answer
    r = run_verify(vtype, **p)
    mark = "PASS-OK" if r.status == expect else "MISMATCH"
    if r.status == expect:
        passed += 1
    print(f"{mark} [{vtype}] answer={answer!r:30} → {r.status:6} 期望{expect:6} | {r.message[:60]}")

print(f"\n=== 验证器测试：{passed}/{len(CASES)} 通过 ===")
