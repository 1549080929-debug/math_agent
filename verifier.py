"""验证器（裁判）：用 SymPy 对子任务结果做确定性验证。

这是整个系统的"奇点"——对话中反复强调的：LLM 是概率生成器，
它不能自证正确；验证器必须来自确定性的符号计算引擎。

状态约定（三态裁判，补丁 P9）：
    PASS   → 验证通过
    FAIL   → 验证失败（触发反馈纠错）
    UNSURE → 验证器看不懂/无法处理（不判错，标记待人工确认）

等价性处理：两个形式不同的表达式（如 sin^2 x 与 1-cos^2 x）
比较一律用 simplify(a-b)==0，而不是 ==；数值情况用误差容忍度。

适配层（裁判监督员）：LLM 常写 "2x-4" 这类缺乘号的表达式，
SymPy 无法直接解析。_sympify 会先尝试原样解析，失败则自动补乘号。

验证类型：
    root             求根验证（代回）
    extreme          驻点验证（一阶导=0）
    interval_extreme 区间最值验证（端点+驻点比较）
    equality         表达式等价验证（simplify 差值）
    satisfies        条件满足验证（支持链式不等式）
    inequality       不等式解集验证（solveset 对解集）
    solution_set     解集等价验证（L3 完备性锚：solveset 求完备真解集，抓漏解/压缩篡改）
"""

import random
import re

import sympy as sp
from sympy.core.relational import Relational

from config import NUMERIC_TOL


class VerifyResult:
    """验证结果：三态 + 人类可读的信息"""

    def __init__(self, status, message=""):
        assert status in ("PASS", "FAIL", "UNSURE")
        self.status = status
        self.message = message

    def __repr__(self):
        return f"VerifyResult({self.status}, {self.message})"

    @property
    def passed(self):
        return self.status == "PASS"


# ---------------------------------------------------------------------------
# 适配层：表达式规范化
# ---------------------------------------------------------------------------

def _insert_implicit_mul(s):
    """把缺乘号的表达式补上乘号：'2x-4' → '2*x-4'，'2(x+1)' → '2*(x+1)'。"""
    s = re.sub(r'(\d)([A-Za-z(])', r'\1*\2', s)   # 数字后跟字母/左括号
    s = re.sub(r'([A-Za-z)])(\d)', r'\1*\2', s)   # 字母/右括号后跟数字
    s = re.sub(r'(\))([A-Za-z(])', r'\1*\2', s)   # 右括号后跟字母/左括号
    return s


def _normalize_unicode(s):
    """Unicode 数学符号归一化：'√3' → 'sqrt(3)'、'×' → '*'、'−' → '-'。"""
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/")
    s = re.sub(r'√\(', 'sqrt(', s)
    s = re.sub(r'√(\d+)', r'sqrt(\1)', s)
    return s


def _sympify(s):
    """把字符串转成 sympy 表达式，兼容 '2x-4' 这类写法与 √ 等 Unicode 符号；失败抛异常。"""
    if isinstance(s, str):
        s = _normalize_unicode(s)
        for cand in (s, _insert_implicit_mul(s)):
            try:
                return sp.sympify(cand)
            except Exception:
                continue
        raise ValueError(f"无法解析表达式：{s}")
    return sp.sympify(s)


# ---------------------------------------------------------------------------
# 验证函数库
# ---------------------------------------------------------------------------

def verify_root(equation, root, var_name="x"):
    """验证：把 root 代入 equation（支持 "expr=0" 或纯 expr 形式），左边应等于 0。"""
    try:
        var = sp.symbols(var_name)
        if "=" in equation:
            lhs_s, rhs_s = equation.split("=", 1)
            lhs, rhs = _sympify(lhs_s), _sympify(rhs_s)
        else:
            lhs, rhs = _sympify(equation), sp.Integer(0)
        root_expr = _sympify(root)
        diff = sp.simplify((lhs - rhs).subs(var, root_expr))
        if diff == 0:
            return VerifyResult("PASS", f"代入 {var_name}={root} 成立")
        # 数值兜底：处理 sqrt(3) 与 1.732... 的写法差异
        if diff.is_number:
            val = complex(diff.evalf())
            if abs(val) < NUMERIC_TOL:
                return VerifyResult("PASS", f"代入后数值 ≈ {diff.evalf():.8f}，在误差容忍度内")
        return VerifyResult("FAIL", f"代入 {var_name}={root} 得 {diff}，不等于 0")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def verify_extreme(expr, point, var_name="x"):
    """验证：point 是 expr 的驻点（一阶导数为 0）。"""
    try:
        var = sp.symbols(var_name)
        e = _sympify(expr)
        p = _sympify(point)
        deriv = sp.diff(e, var)
        dval = sp.simplify(deriv.subs(var, p))
        if dval == 0:
            return VerifyResult("PASS", f"f'({point}) = 0，是驻点")
        if dval.is_number:
            val = complex(dval.evalf())
            if abs(val) < NUMERIC_TOL:
                return VerifyResult("PASS", f"f'({point}) ≈ 0（数值在误差容忍度内）")
        return VerifyResult("FAIL", f"f'({point}) = {dval} ≠ 0，不是驻点")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def verify_interval_extreme(expr, var_name, interval, claimed, which="min", subs=None):
    """验证：函数在闭区间上的最值（最小值或最大值）等于 claimed。

    subs: 额外替换，如 {"a": "sqrt(2)"}——用于含参问题里，
          LLM 求出的参数值先代回表达式再验最值。
    """
    try:
        var = sp.symbols(var_name)
        e = _sympify(expr)
        if subs:
            for k, v in subs.items():
                e = e.subs(sp.symbols(k), _sympify(v))
        a, b = _sympify(interval[0]), _sympify(interval[1])
        claimed_expr = _sympify(claimed)

        # 候选点：两个端点 + 区间内的驻点
        candidates = [(a, sp.simplify(e.subs(var, a))),
                      (b, sp.simplify(e.subs(var, b)))]
        deriv = sp.diff(e, var)
        for x0 in sp.solve(deriv, var):
            try:
                if bool(a <= x0) and bool(x0 <= b):
                    candidates.append((x0, sp.simplify(e.subs(var, x0))))
            except Exception:
                pass

        # 数值比较（避免符号形式不同导致的误判）
        nums = []
        for x0, v in candidates:
            try:
                nums.append((x0, complex(v.evalf())))
            except Exception:
                pass
        if not nums:
            return VerifyResult("UNSURE", "无法对候选点做数值评估")

        label = "最小值" if which == "min" else "最大值"
        best_x, best_v = (min if which == "min" else max)(nums, key=lambda t: t[1].real)
        claimed_num = complex(claimed_expr.evalf())
        if abs(best_v - claimed_num) < NUMERIC_TOL:
            return VerifyResult("PASS", f"区间{label} = {claimed}，与计算值 {best_v.real:.6f}（x={best_x}）一致")
        return VerifyResult("FAIL", f"计算得区间{label} ≈ {best_v.real:.6f}（x≈{best_x}），与声称的 {claimed} 不符")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def _expr_from_eq(s):
    """把 "expr = 0" / "expr = rhs" 转成等价表达式（取左边减右边）。"""
    if isinstance(s, str) and '=' in s:
        lhs_s, rhs_s = s.split('=', 1)
        return _sympify(lhs_s) - _sympify(rhs_s)
    return _sympify(s)


def verify_expression_equality(expr1, expr2):
    """验证两个表达式等价（处理 sin^2 x vs 1-cos^2 x 这类形式不同但相等的答案；
    也支持 "标准形式 = 0" 的写法，如 "x^2-(2m+2)x+m^2+2 = 0"）。"""
    try:
        e1, e2 = _expr_from_eq(expr1), _expr_from_eq(expr2)
        if sp.simplify(e1 - e2) == 0:
            return VerifyResult("PASS", "表达式等价")
        # 数值抽样兜底
        syms = list(e1.free_symbols | e2.free_symbols)
        if not syms:
            return VerifyResult("FAIL", f"{e1} 与 {e2} 不相等")
        ok = True
        for _ in range(5):
            subs = {s: random.uniform(0.5, 3.0) for s in syms}
            try:
                v1 = complex(e1.evalf(subs=subs))
                v2 = complex(e2.evalf(subs=subs))
                if abs(v1 - v2) > 1e-4 * max(1.0, abs(v1), abs(v2)):
                    ok = False
                    break
            except Exception:
                return VerifyResult("UNSURE", "数值抽样失败")
        if ok:
            return VerifyResult("PASS", "表达式数值等价（抽样验证）")
        return VerifyResult("FAIL", f"{expr1} 与 {expr2} 不等价")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def verify_satisfies(condition, value, var_name="x"):
    """验证：value 满足条件（如 x>0、判别式>=0）。支持链式不等式 1<=x<=4。"""
    try:
        var = sp.symbols(var_name)
        v = _sympify(value)

        # 链式不等式 "1 <= x <= 4" → 拆成两个条件分别检查
        ops = re.findall(r'<=|>=|==|<|>', condition)
        parts = [p.strip() for p in re.split(r'<=|>=|==|<|>', condition)]
        if len(ops) == 2 and len(parts) == 3:
            ok = _check_chained(parts[0], parts[2], ops[0], ops[1], v)
            if ok:
                return VerifyResult("PASS", f"条件 {condition} 代入 {var_name}={value} 成立")
            return VerifyResult("FAIL", f"条件 {condition} 代入 {var_name}={value} 不成立")

        rel = _sympify(condition).subs(var, v)
        if rel == True:  # 注意：sympy 返回 BooleanTrue，== 才成立
            return VerifyResult("PASS", f"条件 {condition} 代入 {var_name}={value} 成立")
        if rel == False:
            return VerifyResult("FAIL", f"条件 {condition} 代入 {var_name}={value} 不成立")
        return VerifyResult("UNSURE", f"条件 {condition} 无法数值判定")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def _check_chained(lo_s, hi_s, op_lo, op_hi, v):
    """检查链式不等式：lo_s <op_lo> v <op_hi> hi_s 是否成立。"""
    lo = _sympify(lo_s)
    hi = _sympify(hi_s)
    # 左边界 "lo <op_lo> v" → 检查 v 相对 lo 的关系
    left_ok = {"<": v > lo, "<=": v >= lo, ">": v < lo, ">=": v <= lo, "==": v == lo}[op_lo]
    # 右边界 "v <op_hi> hi" → 检查 v 相对 hi 的关系
    right_ok = {"<": v < hi, "<=": v <= hi, ">": v > hi, ">=": v >= hi, "==": v == hi}[op_hi]
    return bool(left_ok) and bool(right_ok)


def verify_inequality(condition, claimed, var_name="x"):
    """验证：一元不等式 condition 的解集 == LLM 声称的答案。

    condition: 如 "(k+2)**2 - 4 < 0"、"8*m - 4 > 0"
    claimed:   LLM 答案，支持形态："m > 1/2"、"-4 < k < 0"、"0 <= a <= 2"、
               "(-4, 0)"、"[0, 2]"、"a = 0 或 a = 2"、"k < -4 或 k > 0"
    """
    try:
        var = sp.symbols(var_name)
        true_set = sp.solveset(_sympify(condition), var, domain=sp.S.Reals)
        claimed_set = _parse_solution_set(claimed, var)
        if claimed_set is None:
            return VerifyResult("UNSURE", f"无法解析声称的答案：{claimed}")
        if true_set == claimed_set:
            return VerifyResult("PASS", f"解集 {claimed} 与真解集 {true_set} 一致")
        return VerifyResult("FAIL", f"真解集是 {true_set}，声称的 {claimed} 与之不符")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def verify_solution_set(expr, claimed, var_name="x"):
    """L3 锚：解集等价验证（完备性，不只是正确性）。

    用 solveset 求 expr 在 Reals 上的完备真解集，与 LLM 声称的完整解集做
    集合相等比较。这是"求所有解"类问题的完备锚：solveset 是符号完备解器，
    能发现代回验证（verify_root）永远发现不了的"漏掉的候选"，也能抓"区间
    答成点集"这类压缩篡改（P5 模式）。

    expr:    方程或条件，三种形态：
             - 方程   "x**2 - 5*x + 6 = 0"、"x**2 - 5*x + 6"（=0 可省略）
             - 不等式 "a**2 - 2*a <= 0"、"(k+2)**2 - 4 < 0"
    claimed: 声称的完整解集："2 或 3"、"2"、"0 <= a <= 2"、"(-4, 0)"、"sqrt(3)"
    """
    try:
        var = sp.symbols(var_name)
        s = expr.strip() if isinstance(expr, str) else str(expr)
        if "=" in s and not any(op in s for op in ("<", ">")):
            lhs_s, rhs_s = s.split("=", 1)
            target = sp.Eq(_sympify(lhs_s), _sympify(rhs_s))
        else:
            target = _sympify(s)
            if not isinstance(target, Relational):
                target = sp.Eq(target, sp.Integer(0))

        true_set = sp.solveset(target, var, domain=sp.S.Reals)
        claimed_set = _parse_solution_set(claimed, var)
        if claimed_set is None:
            return VerifyResult("UNSURE", f"无法解析声称的答案：{claimed}")

        if true_set == claimed_set:
            return VerifyResult("PASS", f"解集 {claimed} 与真解集 {true_set} 一致（完备）")
        return VerifyResult("FAIL", f"真解集是 {true_set}，声称的 {claimed} 与之不符（漏解或多余候选）")
    except Exception as e:
        return VerifyResult("UNSURE", f"验证器无法处理：{e}")


def _parse_solution_set(s, var):
    """把 LLM 答案解析成 sympy 集合，用于与真解集比较。"""
    s = s.strip()
    if not s:
        return None

    # 0) 并集："m < 1 或 m > 2"、"a = 0 或 a = 2"
    if '或' in s or '∪' in s:
        parts = [p.strip() for p in re.split(r'或|∪', s)]
        sets = [_parse_solution_set(p, var) for p in parts]
        if any(x is None for x in sets):
            return None
        result = sets[0]
        for x in sets[1:]:
            result = sp.Union(result, x)
        return result

    # 1) 区间记号："(-4, 0)"、"[0, 2]"、"(1/2, oo)"
    m = re.match(r'^[\[(]([^,\[\]]+),\s*([^,\[\]]+)[\])]$', s)
    if m:
        lo = _sympify(m.group(1).replace('+oo', 'oo'))
        hi = _sympify(m.group(2).replace('+oo', 'oo'))
        left_open = s.startswith('(')
        right_open = s.endswith(')')
        if left_open and right_open:
            return sp.Interval.open(lo, hi)
        if left_open:
            return sp.Interval.Lopen(lo, hi)
        if right_open:
            return sp.Interval.Ropen(lo, hi)
        return sp.Interval(lo, hi)

    # 2) 链式不等式："0 <= a <= 2"、"-4 < k < 0"
    parts = [p.strip() for p in re.split(r'<=|>=|==|<|>', s)]
    ops = re.findall(r'<=|>=|==|<|>', s)
    if len(parts) == 3 and len(ops) == 2:
        lo = _sympify(parts[0])
        hi = _sympify(parts[2])
        lo_open = ops[0] in ('<', '>')
        hi_open = ops[1] in ('<', '>')
        if lo_open and hi_open:
            return sp.Interval.open(lo, hi)
        if lo_open:
            return sp.Interval.Lopen(lo, hi)
        if hi_open:
            return sp.Interval.Ropen(lo, hi)
        return sp.Interval(lo, hi)

    # 3) 单个关系："m > 1/2"、"x = 2"
    try:
        if re.fullmatch(r'[^<>!=]+=[^<>!=]+', s):
            # "a = 0" → Eq(a, 0)。注意不能 sympify("a==0")（会被 Python == 短路成 bool）
            lhs_s, rhs_s = s.split('=', 1)
            return sp.solveset(sp.Eq(_sympify(lhs_s), _sympify(rhs_s)), var, domain=sp.S.Reals)
        rel = _sympify(s)
        if isinstance(rel, Relational):
            return sp.solveset(rel, var, domain=sp.S.Reals)
    except Exception:
        pass

    # 4) 裸单值："2"、"sqrt(3)"、"-1/2"（不带变量名的单点答案）
    try:
        val = _sympify(s)
        if not isinstance(val, Relational) and not val.free_symbols:
            return sp.FiniteSet(val)
    except Exception:
        pass

    return None


# ---------------------------------------------------------------------------
# 类型系统 + 终局验证（审计修正第 2 波）
# ---------------------------------------------------------------------------

SET_TYPES = ("interval", "point_set", "union", "inequality")


def classify_answer_type(parsed):
    """把解析出的 sympy 集合分类为类型标签。"""
    if parsed is None:
        return None
    if isinstance(parsed, sp.FiniteSet):
        return "point_set" if len(parsed) > 1 else "value"
    if isinstance(parsed, sp.Interval):
        return "interval"
    if isinstance(parsed, sp.Union):
        return "union"
    return None


def verify_answer_type(declared_type, answer, var_name="x"):
    """类型核查：LLM 答案的实际类型是否与拆解时声明的类型一致。

    防 P5 类"压缩篡改"：声明 interval 却答成 point_set → FAIL。
    仅对集合类声明做核查；value 类无法解析为集合 → UNSURE（不误杀）。
    """
    if not declared_type or declared_type not in SET_TYPES:
        return VerifyResult("UNSURE", "仅对集合类答案做类型核查")
    try:
        var = sp.symbols(var_name)
        parsed = _parse_solution_set(answer, var)
        if parsed is None:
            return VerifyResult("UNSURE", f"无法解析答案以核查类型：{answer}")
        actual = classify_answer_type(parsed)
        if actual is None:
            return VerifyResult("UNSURE", "无法分类答案类型")
        # inequality 声明的答案可能表现为 interval/union/point_set
        if actual == declared_type or (declared_type == "inequality" and actual in SET_TYPES):
            return VerifyResult("PASS", f"类型一致：{declared_type}")
        return VerifyResult("FAIL", f"类型不符：声明 {declared_type}，实际 {actual}（{answer}）")
    except Exception as e:
        return VerifyResult("UNSURE", f"类型核查失败：{e}")


def _interval_extrema(f, x, interval):
    """数值化计算 f 在闭区间上的 (min, max)。"""
    a, b = sp.sympify(interval[0]), sp.sympify(interval[1])
    cands = [sp.simplify(f.subs(x, a)), sp.simplify(f.subs(x, b))]
    for x0 in sp.solve(sp.diff(f, x), x):
        try:
            if bool(a <= x0) and bool(x0 <= b):
                cands.append(sp.simplify(f.subs(x, x0)))
        except Exception:
            pass
    nums = [complex(c.evalf()).real for c in cands if c.is_number]
    if not nums:
        raise ValueError("无法数值评估")
    return min(nums), max(nums)


def _sample_points(aset):
    """从集合内部取采样点（区间取端点+中点，点集取各点，并集/交集/补集递归），数值化。"""
    pts = []
    if isinstance(aset, sp.Interval):
        a0, a1 = aset.start, aset.end
        pts = [a0, a1]
        try:
            pts.append((a0 + a1) / 2)
        except Exception:
            pass
    elif isinstance(aset, sp.FiniteSet):
        pts = list(aset)
    elif isinstance(aset, (sp.Union, sp.Intersection, sp.Complement, sp.ConditionSet)):
        for arg in aset.args:
            pts.extend(_sample_points(arg))
    out = []
    for p in pts:
        try:
            n = sp.N(p)
            if n.is_number and n.is_real:
                out.append(n)
        except Exception:
            pass
    return out


def _outside_points(aset):
    """取集合边界外各一点（有界区间端点 ±1，点集取 min-1/max+1）。"""
    pts = []
    def collect(s):
        if isinstance(s, sp.Interval):
            if s.start.is_finite:
                pts.append(s.start - 1)
            if s.end.is_finite:
                pts.append(s.end + 1)
        elif isinstance(s, sp.FiniteSet):
            vals = [float(v.evalf()) for v in s]
            if vals:
                pts.append(sp.Rational(vals[0]) - 1)
                pts.append(sp.Rational(vals[-1]) + 1)
        elif isinstance(s, sp.Union):
            for arg in s.args:
                collect(arg)
    collect(aset)
    return pts


def _compare(val, op, target):
    t = complex(sp.sympify(target).evalf()).real
    return {">=": val >= t - 1e-9, "<=": val <= t + 1e-9,
            ">": val > t, "<": val < t, "==": abs(val - t) < 1e-6}[op]


def verify_final_parameter_set(claimed, expr, var_name="x", param_name="a",
                               interval=None, conditions=None):
    """终局验证：声称的参数集合在区间上满足所有条件。

    conditions: [{"which": "min|max|diff", "op": ">=|<=", "value": "0"}, ...]
    内部点不满足 → FAIL（答案过宽，强证据）；
    外部点全部满足 → 提示可能过窄（弱证据，UNSURE 不误杀）。
    """
    try:
        x = sp.symbols(var_name)
        p = sp.symbols(param_name)
        claimed_set = _parse_solution_set(claimed, p)
        if claimed_set is None:
            return VerifyResult("UNSURE", f"无法解析终局答案：{claimed}")
        conds = conditions or []
        if not conds or not interval:
            return VerifyResult("UNSURE", "终局验证缺少 conditions/interval 参数")

        def check_at(av):
            f = sp.sympify(expr).subs(p, av)
            mn, mx = _interval_extrema(f, x, interval)
            for cond in conds:
                val = {"min": mn, "max": mx, "diff": mx - mn}[cond["which"]]
                if not _compare(val, cond.get("op"), cond.get("value")):
                    return False, f"a={av} 时 {cond['which']}={val:.4f} 不满足 {cond['op']} {cond['value']}"
            return True, ""

        for av in _sample_points(claimed_set):
            ok, msg = check_at(av)
            if not ok:
                return VerifyResult("FAIL", f"答案过宽：{msg}（该点在声称集合内）")
        for av in _outside_points(claimed_set):
            ok, _ = check_at(av)
            if ok:
                return VerifyResult("UNSURE",
                                    f"警告：a={av}（在声称集合外）也满足全部条件，答案可能过窄，请人工确认")
        return VerifyResult("PASS", f"终局验证通过：集合 {claimed} 内 {len(_sample_points(claimed_set))} 个采样点全满足条件")
    except Exception as e:
        return VerifyResult("UNSURE", f"终局验证无法处理：{e}")


# ---------------------------------------------------------------------------
# 分发器
# ---------------------------------------------------------------------------

VERIFIERS = {
    "root": verify_root,
    "extreme": verify_extreme,
    "interval_extreme": verify_interval_extreme,
    "equality": verify_expression_equality,
    "satisfies": verify_satisfies,
    "inequality": verify_inequality,
    "solution_set": verify_solution_set,
    "answer_type": verify_answer_type,
    "final_parameter_set": verify_final_parameter_set,
}


# ---------------------------------------------------------------------------
# 锚定层级（Verification Autonomy Levels，见 docs/05-锚定层级.md）
#   核心变量不是"能力"，而是"信任责任归谁"：
#   L0 LLM 声明（信任递归） / L1 题面派生 / L2 客观真值（正确性）
#   L3 定义性/证明性（单性质完备，ODD 内） / L4 领域级证明系统 / L5 不可判定
# ---------------------------------------------------------------------------
ANCHOR_LEVELS = {
    "root":                ("L2", "代回单根：正确性；完备性盲区"),
    "extreme":             ("L2", "驻点代回：正确性"),
    "interval_extreme":    ("L3", "端点+驻点穷举：二次函数域内单性质完备"),
    "equality":            ("L2", "simplify 等价；数值抽样兜底非完备"),
    "satisfies":           ("L2", "单点满足：正确性"),
    "inequality":          ("L3", "solveset 解集等价：完备"),
    "solution_set":        ("L3", "solveset 解集等价：完备（抓漏解/压缩篡改）"),
    "answer_type":         ("L3", "类型系统：对'类型符合'性质完备"),
    "final_parameter_set": ("L2", "采样验证：正确性；完备性=采样天花板"),
}


def anchor_level(verify_type):
    """返回某验证类型的 VAL 等级与说明（如 ("L3", "solveset 解集等价：完备")）。"""
    return ANCHOR_LEVELS.get(verify_type, ("L0", "未知验证类型"))


def run_verify(verify_type, **kwargs):
    fn = VERIFIERS.get(verify_type)
    if fn is None:
        return VerifyResult("UNSURE", f"未知验证类型：{verify_type}")
    return fn(**kwargs)
