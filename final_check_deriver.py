"""从题面确定性派生终局验证规格（不依赖 LLM 声明）。

审计修正第 3 波：终局验证的信任递归——final_check 若由 LLM 声明可能出错（#8 假 PASS）。
改为规则自动派生：区间、表达式、条件全部从题目文本提取，确定性、可审计。
规则提取失败才回退到 LLM 声明的 final_check。
"""

import re

import sympy as sp

from verifier import _insert_implicit_mul, _sympify

_FUNCS = {"sin", "cos", "tan", "log", "ln", "exp", "sqrt", "abs", "sec", "csc", "cot", "arcsin", "arccos", "arctan"}


def _insert_var_mul(s):
    """在连续字母间补乘号（跳过 sin/sqrt 等函数名）：'2ax' → '2a*x'。"""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isalpha():
            j = i
            while j < len(s) and s[j].isalpha():
                j += 1
            token = s[i:j]
            out.append(token if token in _FUNCS else "*".join(token))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _normalize_expr(s):
    """题目文本里的数学表达式 → SymPy 可解析形式：'x^2-2ax+1' → 'x**2-2*a*x+1'。"""
    return _insert_implicit_mul(_insert_var_mul(s))


def _extract_interval(question):
    m = re.search(r'\[([^\[\]]+?)\s*,\s*([^\[\]]+?)\]', question)
    if not m:
        return None
    return [m.group(1).strip(), m.group(2).strip()]


def _extract_expr(question):
    # f(x)=... 形式
    m = re.search(r'f\(x\)\s*=\s*([^\s，。；,;]+)', question)
    if m:
        return m.group(1).strip()
    # 不等式形式："不等式 x^2-2kx+k^2-1 ≥ 0"
    m = re.search(r'不等式\s*([^\s≥≤>]+)', question)
    if m:
        return m.group(1).strip()
    return None


def _extract_conditions(question):
    """从中文条件模式提取 (which, op, value)。规则表：可扩展。"""
    conds = []
    pats = [
        (r'最小值不小于\s*(-?[\d.]+)', "min", ">="),
        (r'最小值大于等于\s*(-?[\d.]+)', "min", ">="),
        (r'最小值不超过\s*(-?[\d.]+)', "min", "<="),
        (r'最小值小于等于\s*(-?[\d.]+)', "min", "<="),
        (r'最小值为\s*(-?[\d.]+)', "min", "=="),
        (r'最大值不小于\s*(-?[\d.]+)', "max", ">="),
        (r'最大值大于等于\s*(-?[\d.]+)', "max", ">="),
        (r'最大值不超过\s*(-?[\d.]+)', "max", "<="),
        (r'最大值小于等于\s*(-?[\d.]+)', "max", "<="),
        (r'最大值为\s*(-?[\d.]+)', "max", "=="),
        (r'最大值与最小值之差为\s*(-?[\d.]+)', "diff", "=="),
    ]
    for pat, which, op in pats:
        for m in re.finditer(pat, question):
            conds.append({"which": which, "op": op, "value": m.group(1)})

    # 恒成立型："不等式 ... ≥ v 对一切 x∈[a,b] 恒成立" → min ≥ v
    m = re.search(r'不等式\s*\S+\s*([≥>]=?)\s*(-?[\d.]+)', question)
    if m and ("恒成立" in question or "一切" in question or "对任意" in question):
        op = ">=" if m.group(1).startswith(("≥", ">")) else "<="
        conds.append({"which": "min", "op": op, "value": m.group(2)})
    return conds or None


def _extract_param(expr, question):
    try:
        free = set(_sympify(_normalize_expr(expr)).free_symbols) - {sp.symbols("x")}
    except Exception:
        return None
    if len(free) == 1:
        return str(free.pop())
    # 多个参数时用"求(实数) X"的目标
    m = re.search(r'求(?:实数)?\s*([a-zA-Z])', question)
    if m and m.group(1) != "f":
        cand = sp.symbols(m.group(1))
        if cand in free:
            return m.group(1)
    return None


def derive_final_check(question):
    """返回 (final_check, reason)。reason: 'rule' | 'no_interval' | 'no_expr' | ..."""
    interval = _extract_interval(question)
    expr = _extract_expr(question)
    conds = _extract_conditions(question)
    if not interval:
        return None, "no_interval"
    if not expr:
        return None, "no_expr"
    if not conds:
        return None, "no_condition"
    # 区间边界必须是数值（符号边界如 [0,m] 无法数值化）
    try:
        for b in interval:
            v = _sympify(b)
            if not v.is_number:
                return None, "symbolic_interval"
    except Exception:
        return None, "bad_interval"
    param = _extract_param(expr, question)
    if not param:
        return None, "no_param"
    fc = {
        "type": "final_parameter_set",
        "params": {
            "expr": _normalize_expr(expr),
            "var_name": "x",
            "param_name": param,
            "interval": interval,
            "conditions": conds,
        },
    }
    return fc, "rule"


if __name__ == "__main__":
    import json

    with open("data/problems_20.json", encoding="utf-8") as f:
        problems = json.load(f)
    n_derived = 0
    for p in problems:
        fc, reason = derive_final_check(p["question"])
        if fc:
            n_derived += 1
            print(f"  [派生] #{p['id']} L{p['level']} params={fc['params']['param_name']} "
                  f"interval={fc['params']['interval']} conds={fc['params']['conditions']}")
        else:
            print(f"  [跳过] #{p['id']} L{p['level']} ({reason})")
    print(f"\n派生覆盖率：{n_derived}/{len(problems)}")
