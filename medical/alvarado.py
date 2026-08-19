"""Alvarado 评分（MANTRELS）：已验证的阑尾炎决策规则——第三章的 L3 锚。

来源：Alvarado A. "A practical score for the early diagnosis of acute appendicitis."
     Ann Emerg Med, 1986. 八项：M 转移痛(1) A 厌食(1) N 恶心呕吐(1)
     T 右下腹压痛(2) R 反跳痛(1) E 发热>37.3℃(1) L 白细胞>10(2) S 中性粒>75%(1)。
     满分 10：≥7 高风险，4–6 中风险，≤3 低风险。

L3 属性（对照 docs/05-锚定层级.md）：
- 外部已验证规则（非自造阈值）；
- 输入是客观字段（病史/体征/化验，可确定性解析）；
- 决策边界可判定（≥7/4–6/≤3）；
- **缺数据语义**：输入缺失时返回可达分数区间 [min,max]——规则自己"拒绝完整打分"，
  而不是像手写规则那样靠人拍一个阈值。

ODO（可判定域）：疑似阑尾炎（确诊标签含"阑尾炎"或主诉/病史含"右下腹"）。
"""

import re

# ---------------------------------------------------------------------------
# 八项提取（确定性解析，缺项返回 None）
# ---------------------------------------------------------------------------

def _has(s, *kw):
    return any(k in s for k in kw)


def _parse_mantrels(case):
    """从病例自由文本提取八项，返回 {item: 0/1/2 或 None(未知)}。"""
    history = case.get("history", "")
    exam = case.get("exam", "")
    lab = case.get("lab", "")
    hx_exam = history + " " + exam

    # M 转移痛：脐周/上腹 → 右下腹 为有；"无转移" 为无
    if "无转移" in history:
        m = 0
    elif re.search(r"(脐周|上腹|中腹).{0,12}(右下腹)", history):
        m = 1
    elif "转移" in history:
        m = 1
    else:
        m = None

    # A 厌食/食欲减退（先判否定，避免"无食欲"误判）
    if _has(history, "食欲正常", "食欲好", "无食欲"):
        a = 0
    elif _has(history, "食欲减退", "食欲差", "厌食"):
        a = 1
    else:
        a = None

    # N 恶心/呕吐：恶心与呕吐各自独立判定，任一阳性即 1（"伴恶心、无呕吐"应计 1）
    nausea_pos = ("恶心" in history) and ("无恶心" not in history) and ("不伴恶心" not in history)
    vomit_pos = ("呕吐" in history) and ("无呕吐" not in history)
    if nausea_pos or vomit_pos:
        n = 1
    elif ("无恶心" in history) or ("无呕吐" in history) or ("不伴恶心" in history):
        n = 0
    else:
        n = None

    # T 右下腹压痛（2 分）
    if "右下腹" in exam and "压痛" in exam and "无压痛" not in exam:
        t = 2
    elif "右下腹" in exam and "无压痛" in exam:
        t = 0
    else:
        t = None

    # R 反跳痛
    if "反跳痛" in exam:
        r = 1 if "无反跳" not in exam else 0
    else:
        r = None

    # E 发热 >37.3℃（体温优先；无体温则看"发热"字样）
    mtemp = re.search(r"体温\s*([\d.]+)", exam)
    if mtemp:
        e = 1 if float(mtemp.group(1)) > 37.3 else 0
    elif "发热" in hx_exam and "无发热" not in hx_exam:
        e = 1
    elif "无发热" in hx_exam:
        e = 0
    else:
        e = None

    # L 白细胞 >10（2 分）
    mwbc = re.search(r"WBC\s*([\d.]+)", lab) or re.search(r"白细胞[^0-9]*([\d.]+)", lab)
    if mwbc:
        l = 2 if float(mwbc.group(1)) > 10 else 0
    else:
        l = None

    # S 中性粒细胞比例 >75%
    msh = re.search(r"中性粒[^0-9]*([\d.]+)\s*%", lab)
    if msh:
        s = 1 if float(msh.group(1)) > 75 else 0
    else:
        s = None

    return {"M": m, "A": a, "N": n, "T": t, "R": r, "E": e, "L": l, "S": s}


def alvarado_range(case):
    """返回 (min_score, max_score, missing_items, items)。缺项用 [0, 满分] 取界。"""
    items = _parse_mantrels(case)
    score = {"M": 1, "A": 1, "N": 1, "T": 2, "R": 1, "E": 1, "L": 2, "S": 1}
    mn = mx = 0
    missing = []
    for k in ("M", "A", "N", "T", "R", "E", "L", "S"):
        v = items[k]
        if v is None:
            missing.append(k)
            mx += score[k]
        else:
            mn += v
            mx += v
    return mn, mx, missing, items


def risk_label(score):
    if score >= 7:
        return "high"
    if score >= 4:
        return "moderate"
    return "low"


def in_odd(case):
    """可判定域：疑似阑尾炎。"""
    d = case.get("confirmed_diagnosis", "")
    cc = case.get("chief_complaint", "") + case.get("history", "")
    return ("阑尾炎" in d) or ("右下腹" in cc)


UNCERTAINTY = ["无法确诊", "不能确定", "待查", "待鉴别", "需进一步", "需检查",
               "尚不能", "无法排除", "待完善", "需除外", "倾向", "考虑", "可能", "待定", "疑似"]


def check(case, llm_out):
    """对疑似阑尾炎病例，用 Alvarado 判定 LLM 诊断是否与规则决策边界一致。

    返回 (PASS/FAIL/WARN/N/A, message)。
    """
    if not in_odd(case):
        return ("N/A", "非阑尾炎 ODD，Alvarado 不适用")
    mn, mx, missing, items = alvarado_range(case)
    diag = llm_out.get("most_likely_diagnosis", "")
    conf = llm_out.get("confidence", 0)
    is_appendix = "阑尾炎" in diag
    has_uncertainty = any(m in diag for m in UNCERTAINTY)

    if not missing:
        score = mn  # 完整时 mn==mx
        label = risk_label(score)
        if label == "high":
            if is_appendix:
                return ("PASS", f"Alvarado={score}（高风险），诊断阑尾炎一致")
            return ("FAIL", f"Alvarado={score}（高风险），LLM 未诊断阑尾炎（{diag}）")
        if label == "low" and is_appendix and not has_uncertainty and conf > 0.6:
            return ("WARN", f"Alvarado={score}（低风险），确定性阑尾炎诊断需谨慎")
        return ("PASS", f"Alvarado={score}（{label}），诊断与风险一致")

    # 缺数据：规则拒绝完整打分，返回可达区间
    if mn >= 7:
        # 区间下限已到高风险：即使缺项也能确证高风险
        if is_appendix:
            return ("PASS", f"Alvarado≥{mn}（缺 {len(missing)} 项仍达高风险），诊断阑尾炎一致")
        return ("FAIL", f"Alvarado≥{mn}（高风险），LLM 未诊断阑尾炎（{diag}）")
    if mx <= 3:
        if is_appendix and not has_uncertainty and conf > 0.6:
            return ("WARN", f"Alvarado≤{mx}（低风险），确定性阑尾炎诊断需谨慎")
        return ("PASS", f"Alvarado≤{mx}（低风险），诊断与风险一致")
    # 区间不确定（如 3–8）：规则无法支持确定性结论
    if is_appendix and not has_uncertainty and conf > 0.6:
        return ("FAIL", f"Alvarado 区间 {mn}–{mx}（缺 {len(missing)} 项：{''.join(missing)}），"
                         f"数据不足以支持确定性阑尾炎诊断（conf={conf}）")
    if is_appendix:
        return ("PASS", f"Alvarado 区间 {mn}–{mx}，LLM 自带不确定性，可接受")
    return ("PASS", f"Alvarado 区间 {mn}–{mx}，诊断与风险一致")


# ---------------------------------------------------------------------------
# 自测（无需 API）
# ---------------------------------------------------------------------------

def self_test():
    cases = [
        # (名称, 病例片段, 期望 (min,max) 或 None 表示只验 PASS/FAIL)
        ("教科书#1 完整", {"confirmed_diagnosis": "急性阑尾炎", "chief_complaint": "右下腹痛 1 天",
                           "history": "1 天前脐周隐痛，6 小时前转移至右下腹并加重，伴恶心、食欲减退，无呕吐腹泻",
                           "exam": "右下腹麦氏点固定压痛、反跳痛，无肌紧张；体温 37.8℃",
                           "lab": "血常规：WBC 13.5×10^9/L，中性粒细胞 85%"}, (10, 10)),
        ("老年#101", {"confirmed_diagnosis": "急性阑尾炎（老年人不典型表现）", "chief_complaint": "右下腹不适 2 天",
                      "history": "2 天前开始右下腹隐痛，程度较轻，无转移性疼痛，食欲差，无发热，无呕吐",
                      "exam": "右下腹轻度压痛，无反跳痛；体温 37.2℃",
                      "lab": "血常规：WBC 10.2×10^9/L，中性粒细胞 78%"}, (6, 6)),
        ("信息不足#103", {"confirmed_diagnosis": "信息不足，无法确诊（阑尾炎/妇科急症/泌尿系结石待鉴别）",
                          "chief_complaint": "右下腹痛 6 小时",
                          "history": "6 小时前右下腹痛，持续性，伴恶心，无不规律出血，无发热，无尿路症状。未做任何检查",
                          "exam": "右下腹压痛，无反跳痛；生命体征平稳",
                          "lab": "暂无检查结果"}, (3, 8)),
        ("腹泻型#109", {"confirmed_diagnosis": "急性阑尾炎（以腹泻为表现的少见类型）", "chief_complaint": "腹泻 8 次伴腹痛 1 天",
                        "history": "1 天前腹泻 8 次（水样便），脐周痛后转移至右下腹，伴恶心，无发热",
                        "exam": "右下腹固定压痛，轻反跳痛；肠鸣音活跃",
                        "lab": "血常规：WBC 13.0×10^9/L；便常规：未见红白细胞"}, (7, 9)),
    ]
    ok = True
    for name, case, expect in cases:
        mn, mx, missing, _ = alvarado_range(case)
        good = (mn, mx) == expect
        ok &= good
        print(f"{'OK ' if good else 'XX '}{name}: Alvarado 区间 [{mn},{mx}] 缺:{''.join(missing) or '无'}"
              + (f" 期望 {expect}" if not good else ""))
    print(f"\n=== alvarado 自测：{'全部通过' if ok else '有失败'} ===")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if self_test() else 1)
