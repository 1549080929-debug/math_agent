"""对抗性预测实验的"标准答案"审计：用 SymPy 裁判钉死真答案。

实验暴露的问题：LLM 生成的 5 个"标准答案"里，有 3 个可能错了。
这里用确定性符号计算逐题验证，作为复盘的硬证据。
"""

import sympy as sp

x, a, m = sp.symbols('x a m')
print("=" * 60)
print("审计 1：f(x)=(x-a)^2-1 在 [0,2] 上最大值 = 3，求 a 的所有值")
print("=" * 60)

# f(0)=a^2-1, f(2)=(a-2)^2-1，最大值 = max 两者 - 1 = 3 → max(a^2, (a-2)^2) = 4
cands = sp.solve(sp.Eq(a**2, 4), a) + sp.solve(sp.Eq((a - 2)**2, 4), a)
sols = []
for c in cands:
    c = sp.simplify(c)
    mx = sp.Max(sp.simplify((c)**2), sp.simplify((c - 2)**2))
    if sp.simplify(mx - 4) == 0:
        sols.append(c)
print("  真答案（SymPy 验证）：", sorted(sols, key=float))
for c in [-1, 3]:  # 预测表声称的答案
    mx = sp.Max(c**2, (c - 2)**2)
    print(f"  预测表答案 a={c} 验证：max(a^2,(a-2)^2)={mx} ≠ 4 → 不成立")

print()
print("=" * 60)
print("审计 2：x^2-(2m+2)x+(m^2+2)=0 有两个不同交点 → 判别式 > 0")
print("=" * 60)
delta = sp.expand((2 * m + 2)**2 - 4 * (m**2 + 2))
print("  判别式 Δ =", delta)
ineq_sol = sp.solve_univariate_inequality(delta > 0, m)
print("  Δ>0 的解集（SymPy）：", ineq_sol)
for v in [-1, 0, 1]:  # 预测表声称 m<1 成立
    print(f"  m={v}：Δ = {sp.simplify(delta.subs(m, v))} → {'无交点' if sp.simplify(delta.subs(m, v)) < 0 else '有交点'}")
for v in [0.75, 2]:  # 真解集 m>1/2 内的点
    print(f"  m={v}：Δ = {sp.simplify(delta.subs(m, v))} > 0 → 两个交点 ✓")

print()
print("=" * 60)
print("审计 3：f(x)=(x-a)^2-1 在 [0,2] 上最小值 = -1，求 a 的所有值")
print("=" * 60)

def min_on_02(aval):
    """(x-a)^2-1 在 [0,2] 上的最小值"""
    f = (x - aval)**2 - 1
    # 候选：端点 + 顶点（若在区间内）
    cands = [sp.simplify(f.subs(x, 0)), sp.simplify(f.subs(x, 2))]
    if 0 <= aval <= 2:
        cands.append(sp.simplify(f.subs(x, aval)))
    return min(float(sp.simplify(c).evalf()) for c in cands)

for aval in [0, 1, 2, 3, -1]:
    mn = min_on_02(aval)
    ok = abs(mn - (-1)) < 1e-9
    print(f"  a={aval}：最小值 = {mn} {'✓ 满足' if ok else '✗ 不满足'}")
print("  结论：真答案 = 0 ≤ a ≤ 2（整个区间内任意值）")
