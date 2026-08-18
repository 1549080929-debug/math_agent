"""审计两道新题（A 竞赛 / B 多步新题）的标准答案（SymPy）。"""

import sympy as sp
from verifier import verify_interval_extreme

x, a = sp.symbols('x a')

print("=== 题 A 审计：f=x^2-2ax+1 在 [0,3] 上 最大值-最小值=4，答案 a=1 或 2 ===")
for aval, expect in [(1, True), (2, True), (0, False), (3, False), (1.5, False)]:
    mn = verify_interval_extreme("x**2 - 2*a*x + 1", "x", ["0", "3"],
                                 "0", "min", subs={"a": str(aval)})
    # 对候选做 min/max 差值检查
    minv = sp.Min(
        sp.simplify((x**2 - 2*aval*x + 1).subs(x, 0)),
        sp.simplify((x**2 - 2*aval*x + 1).subs(x, 3)),
        *([sp.simplify((x**2 - 2*aval*x + 1).subs(x, aval))] if 0 <= aval <= 3 else [])
    )
    maxv = sp.Max(
        sp.simplify((x**2 - 2*aval*x + 1).subs(x, 0)),
        sp.simplify((x**2 - 2*aval*x + 1).subs(x, 3)),
    )
    diff = float(sp.simplify(maxv - minv).evalf())
    ok = abs(diff - 4) < 1e-9
    print(f"  a={aval}: 差={diff:.4f} 期望{'满足' if expect else '不满足'} → {'PASS' if ok == expect else 'FAIL'}")

print()
print("=== 题 B 审计：f=x^2-2ax+1 在 [0,2] 上 最小≥0 且 最大≤5，答案 0≤a≤1 ===")
for aval in [0, 0.5, 1, -0.5, 2]:
    f = x**2 - 2*aval*x + 1
    vals = [float(sp.simplify(f.subs(x, 0)).evalf()), float(sp.simplify(f.subs(x, 2)).evalf())]
    if 0 <= aval <= 2:
        vals.append(float(sp.simplify(f.subs(x, aval)).evalf()))
    mn, mx = min(vals), max(vals)
    ok_cond = (mn >= 0) and (mx <= 5)
    expect = 0 <= aval <= 1
    print(f"  a={aval}: min={mn:.2f} max={mx:.2f} 满足条件={ok_cond} 期望={expect} → {'PASS' if ok_cond == expect else 'FAIL'}")
