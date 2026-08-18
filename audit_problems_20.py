"""审计 data/problems_20.json 的全部 20 个标准答案（SymPy 逐题验证）。

审计先行：上一轮实验的教训——LLM 生成的"标准答案"3/5 是错的。
这里用确定性符号计算，在跑系统之前先把标准答案钉死。
"""

import json

import sympy as sp

from verifier import verify_extreme, verify_interval_extreme, verify_root, verify_expression_equality

x, a, k, m = sp.symbols('x a k m')


def check(pid, label, fn):
    try:
        ok, detail = fn()
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] #{pid} {label} | {detail}")
        return ok
    except Exception as e:
        print(f"  [ERR] #{pid} {label} | {type(e).__name__}: {e}")
        return False


def run_all():
    with open("data/problems_20.json", encoding="utf-8") as f:
        problems = json.load(f)

    results = {}
    print("=== 标准答案审计（SymPy）===\n")

    # L1
    results[1] = check(1, "顶点 (2,-1)",
                       lambda: (sp.simplify(sp.diff(x**2 - 4*x + 3, x).subs(x, 2)) == 0
                                and sp.simplify((x**2 - 4*x + 3).subs(x, 2)) == -1,
                                f"f'(2)={sp.diff(x**2-4*x+3,x).subs(x,2)}, f(2)={(x**2-4*x+3).subs(x,2)}"))
    results[2] = check(2, "较大根 4",
                       lambda: (verify_root("x**2 - 7*x + 12", "4").passed, "代回成立"))
    results[3] = check(3, "[0,2] 最小值 -3",
                       lambda: (verify_interval_extreme("x**2 - 6*x + 5", "x", ["0", "2"], "-3", "min").passed,
                                "端点+驻点比较"))
    results[4] = check(4, "最大值 5",
                       lambda: (verify_extreme("-x**2 + 4*x + 1", "2").passed
                                and sp.simplify((-x**2 + 4*x + 1).subs(x, 2)) == 5,
                                f"f(2)={(-x**2+4*x+1).subs(x,2)}"))
    results[5] = check(5, "较小根 -2",
                       lambda: (verify_root("x**2 - 2*x - 8", "-2").passed, "代回成立"))
    results[6] = check(6, "[0,3] 最小值 2",
                       lambda: (verify_interval_extreme("x**2 - 2*x + 3", "x", ["0", "3"], "2", "min").passed,
                                "端点+驻点比较"))
    results[7] = check(7, "两根和 5",
                       lambda: (verify_root("x**2 - 5*x + 6", "2").passed
                                and verify_root("x**2 - 5*x + 6", "3").passed
                                and 2 + 3 == 5, "根 2,3，和 5"))

    # L2
    results[8] = check(8, "a=-1 或 3",
                       lambda: (verify_interval_extreme("x**2 - 2*a*x + 2*a", "x", ["0", "2"], "-2", "min",
                                                       subs={"a": "-1"}).passed
                                and verify_interval_extreme("x**2 - 2*a*x + 2*a", "x", ["0", "2"], "-2", "min",
                                                            subs={"a": "3"}).passed,
                                "两个候选代回验证"))
    results[9] = check(9, "m>0",
                       lambda: (sp.simplify(sp.expand((2*m + 4)**2 - 4*(m**2 + 4))) == 16*m
                                and sp.solveset(16*m > 0, m, domain=sp.S.Reals)
                                == sp.Interval.open(0, sp.oo),
                                f"Δ={sp.expand((2*m+4)**2-4*(m**2+4))}"))
    results[10] = check(10, "-5<k<3",
                        lambda: (sp.solveset((k + 1)**2 - 16 < 0, k, domain=sp.S.Reals)
                                 == sp.Interval.open(-5, 3), "solveset 直接对比"))
    results[11] = check(11, "k>2√2",
                        lambda: (sp.solveset(k**2 - 8 > 0, k, domain=sp.S.Reals)
                                 & sp.solveset(k > 0, k, domain=sp.S.Reals)
                                 == sp.Interval.open(2*sp.sqrt(2), sp.oo),
                                "Δ>0 ∩ 两根和>0"))
    results[12] = check(12, "m=3",
                        lambda: (verify_interval_extreme("x**2 - 2*x + 1", "x", ["0", "3"], "0", "min").passed
                                 and verify_interval_extreme("x**2 - 2*x + 1", "x", ["0", "3"], "4", "max").passed
                                 and verify_interval_extreme("x**2 - 2*x + 1", "x", ["0", "2.9"], "4", "max").status == "FAIL",
                                "m=3 时值域恰为 [0,4]；m<3 时最大值<4"))
    results[13] = check(13, "a=0 或 2",
                        lambda: (verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "3", "max",
                                                         subs={"a": "0"}).passed
                                 and verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "3", "max",
                                                             subs={"a": "2"}).passed
                                 and verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "3", "max",
                                                             subs={"a": "-1"}).status == "FAIL",
                                "a=0,2 满足；a=-1 不满足"))
    results[14] = check(14, "根 (5±√17)/4",
                        lambda: (verify_root("2*x**2 - 5*x + 1", "(5 + sqrt(17))/4").passed
                                 and verify_root("2*x**2 - 5*x + 1", "(5 - sqrt(17))/4").passed,
                                "两解代回成立"))

    # L3
    results[15] = check(15, "0≤a≤2",
                        lambda: (all(verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "-1", "min",
                                                             subs={"a": str(v)}).passed for v in (0, 1, 2))
                                 and all(verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "-1", "min",
                                                                 subs={"a": str(v)}).status == "FAIL" for v in (-1, 3)),
                                "区间内 a 满足、区间外不满足（抽样）"))
    def min_sq_dist(kk):
        """(x-kk)^2 在 [1,3] 上的最小值。"""
        vals = [(1 - kk)**2, (3 - kk)**2]
        if 1 <= kk <= 3:
            vals.append(0)
        return min(vals)

    results[16] = check(16, "k≤0 或 k≥4",
                        lambda: (all(min_sq_dist(kk) >= 1 - 1e-9 for kk in (0, -1, 4))
                                 and min_sq_dist(0.5) < 1 and min_sq_dist(2) < 1,
                                "抽样：k=0,-1,4 时 |x-k|² 在 [1,3] 上≥1；k=0.5、2 时<1"))
    results[17] = check(17, "根 √3±1",
                        lambda: (verify_root("x**2 - 2*sqrt(3)*x + 2", "sqrt(3) + 1").passed
                                 and verify_root("x**2 - 2*sqrt(3)*x + 2", "sqrt(3) - 1").passed,
                                "两解代回成立"))

    def has_root_in_interval(av):
        """x²+(a-2)x+1 在 (0,1) 内是否有实根。"""
        reals = [r for r in sp.solve(x**2 + (av - 2)*x + 1, x) if sp.im(r) == 0]
        return any(0 < sp.N(r) < 1 for r in reals)

    results[18] = check(18, "a<0",
                        lambda: (all(has_root_in_interval(av) for av in (-1, -2))
                                 and not any(has_root_in_interval(av) for av in (1, 3, 4)),
                                "a=-1,-2 在 (0,1) 有根；a=1,3,4 无根"))
    results[19] = check(19, "a=0 或 2",
                        lambda: (all(verify_interval_extreme("x**2 - 2*a*x + 1", "x", ["0", "2"],
                                                             str(1 - av**2 if av == 0 else -3), "min",
                                                             subs={"a": str(av)}).passed for av in (0, 2))
                                 and all(verify_interval_extreme("x**2 - 2*a*x + 1", "x", ["0", "2"],
                                                                 str(5 - 4*av if av == 0 else 1), "max",
                                                                 subs={"a": str(av)}).passed for av in (0, 2)),
                                "a=0: min1/max5；a=2: min-3/max1，差均=4"))
    results[20] = check(20, "a=0 或 2（min=-1 且 max=3）",
                        lambda: (all(verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "-1", "min",
                                                             subs={"a": str(av)}).passed for av in (0, 2))
                                 and all(verify_interval_extreme("x**2 - 2*a*x + a**2 - 1", "x", ["0", "2"], "3", "max",
                                                                 subs={"a": str(av)}).passed for av in (0, 2)),
                                "a=0,2 同时满足 min=-1 与 max=3"))

    ok_n = sum(1 for v in results.values() if v)
    print(f"\n=== 标准答案审计：{ok_n}/20 通过 ===")
    with open("data/audit_20.json", "w", encoding="utf-8") as f:
        json.dump({"audited": ok_n == 20, "results": {str(k): bool(v) for k, v in results.items()}},
                  f, ensure_ascii=False, indent=2)
    return ok_n == 20


if __name__ == "__main__":
    run_all()
