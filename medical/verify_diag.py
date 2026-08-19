"""第三章裁判可行性：三个结构性检查（先测裁判本身，再谈架构）。

1. 信息完整性：lab 完全缺失 + 确定性高置信度诊断 = 过度自信（FAIL）
   —— 只对"完全信息缺失"（暂无检查结果/未做任何检查）触发，部分缺失（如"血糖未测"）
      不触发（临床合理，LLM 正确识别所需检查即可）。
2. 红旗征：病例带红旗 → LLM 必须 urgent=True 且列出红旗。
3. 鉴别完整性：确诊标签应出现在鉴别列表或最可能诊断中（漏鉴别 = 覆盖盲区）。
"""

import json
import os

from alvarado import check as check_alvarado

HERE = os.path.dirname(os.path.abspath(__file__))

UNCERTAINTY_MARKERS = ["无法确诊", "不能确定", "待查", "待鉴别", "需进一步", "需检查",
                       "尚不能", "无法排除", "待完善", "需除外", "倾向", "考虑", "可能", "待定", "疑似"]

TOTAL_ABSENCE_MARKERS = ["暂无检查结果", "无检查结果", "无辅助检查", "未做任何检查", "暂无检查", "无任何检查"]


def core_term(d):
    return d.split("（")[0].split("(")[0].strip()

# 诊断同义词归一化（裁判的"等价性处理"，对应数学章的 simplify(a-b)==0）
SYNONYMS = {
    "化脓性脑膜炎": ["细菌性脑膜炎"],
    "格雷夫斯病": ["graves", "格雷夫斯"],
    "慢阻肺急性加重": ["慢性阻塞性肺疾病急性加重", "aecopd"],
    "急性阑尾炎": ["阑尾炎"],
    "糖尿病酮症酸中毒": ["酮症酸中毒", "dka"],
    "输尿管结石": ["泌尿系结石", "尿路结石", "肾结石"],
    "急性胰腺炎": ["胰腺炎"],
    "急性肺栓塞": ["肺栓塞"],
    "急性st段抬高型心肌梗死": ["st段抬高", "stem", "心梗", "心肌梗死"],
    "非st段抬高型心肌梗死": ["非st", "nstem", "心梗", "心肌梗死", "不稳定型心绞痛"],
    "急性下壁心肌梗死": ["下壁", "心肌梗死", "心梗"],
    "甲状腺功能亢进症": ["甲亢", "甲状腺功能亢进"],
    "带状疱疹": ["疱疹"],
    "胃食管反流病": ["胃食管反流"],
    "慢阻肺": ["慢性阻塞性肺疾病"],
}


def diag_mentioned(confirmed_core, joined_lower):
    """确诊核心词是否在 LLM 输出中被提到（含同义词、大小写归一）。"""
    if confirmed_core.lower() in joined_lower:
        return True
    for syn in SYNONYMS.get(confirmed_core, []):
        if syn.lower() in joined_lower:
            return True
    return False


def check_info(case, out):
    lab = case.get("lab", "")
    if not any(m in lab for m in TOTAL_ABSENCE_MARKERS):
        return ("N/A", "信息非完全缺失")
    diag = out.get("most_likely_diagnosis", "")
    conf = out.get("confidence", 0)
    if any(m in diag for m in UNCERTAINTY_MARKERS):
        return ("PASS", f"诊断自带不确定性（{diag}）")
    if conf > 0.6:
        return ("FAIL", f"信息完全缺失仍给确定性诊断（conf={conf}）")
    return ("PASS", f"信息缺失且置信度低（conf={conf}）")


EMERGENCY_TERMS = ["紧急", "危象", "致命", "红旗", "必须识别", "需紧急", "急诊", "紧急处理"]


def check_redflag(case, out):
    rf = case.get("red_flags", "")
    if not rf or rf.startswith("无"):
        return ("N/A", "无红旗")
    urgent = out.get("urgent_action_needed")
    noted = out.get("red_flags_noted", [])
    is_emergency = any(t in rf for t in EMERGENCY_TERMS)
    if is_emergency:
        if urgent is True and noted:
            return ("PASS", "急诊红旗识别+紧急处理正确")
        if urgent is True:
            return ("WARN", "紧急处理正确但未列红旗")
        return ("FAIL", "急诊红旗未触发紧急处理")
    # 临床注意事项（非急诊）：有鉴别/处理即可，不强制 urgent
    if noted or urgent is True:
        return ("PASS", "临床注意事项已覆盖")
    return ("WARN", "临床注意事项未被显式回应")


def check_diff(case, out):
    confirmed = case.get("confirmed_diagnosis", "")
    if confirmed.startswith(("信息不足", "待查", "需首先")):
        return ("N/A", "确诊为'信息不足/行动指令'，跳过鉴别检查")
    core = core_term(confirmed)
    joined = " ".join(out.get("differential_diagnosis", [])) + " " + out.get("most_likely_diagnosis", "")
    joined_lower = joined.lower()
    if diag_mentioned(core, joined_lower):
        return ("PASS", "确诊在鉴别/诊断中")
    return ("FAIL", f"确诊'{core}'不在鉴别列表中")


def main():
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as f:
        cases = {c["id"]: c for c in json.load(f)["cases"]}
    with open(os.path.join(HERE, "cases_hard.json"), encoding="utf-8") as f:
        cases.update({c["id"]: c for c in json.load(f)["cases"]})

    results = {}
    for fname in ("data_baseline.json", "data_baseline_hard.json"):
        with open(os.path.join(HERE, fname), encoding="utf-8") as f:
            for d in json.load(f):
                results[d["id"]] = d

    print(f"{'#':>4} {'类别':<8} {'信息':<6} {'红旗':<6} {'鉴别':<6} {'阿瓦':<6} 判定")
    print("-" * 82)
    gold_fail = {103, 104}   # 人工金标：信息不足仍硬猜
    flagged = []
    for cid in sorted(cases):
        c = cases[cid]
        out = results[cid]["llm_output"]
        i = check_info(c, out)
        r = check_redflag(c, out)
        d = check_diff(c, out)
        a = check_alvarado(c, out)
        is_fail = any(x[0] == "FAIL" for x in (i, r, d, a))
        if is_fail:
            flagged.append(cid)
        cat = c["category"][:6]
        print(f"{cid:>4} {cat:<8} {i[0]:<6} {r[0]:<6} {d[0]:<6} {a[0]:<6} "
              + ("❌ " + "; ".join(x[1] for x in (i, r, d, a) if x[0] == "FAIL") if is_fail else "✅"))

    # 评估
    tp = len(set(flagged) & gold_fail)
    fp = len(set(flagged) - gold_fail)
    fn = len(gold_fail - set(flagged))
    prec = tp / (tp + fp) if (tp + fp) else 0
    rec = tp / (tp + fn) if (tp + fn) else 0
    print("\n" + "=" * 72)
    print(f"裁判评估（金标 = 人工判定 #103/#104 为过度自信）")
    print(f"  命中(TP)={tp}  误报(FP)={fp}  漏报(FN)={fn}")
    print(f"  精确率={prec:.2f}  召回率={rec:.2f}")
    print(f"  被标记: {flagged}（金标: {sorted(gold_fail)}）")
    print("=" * 72)


if __name__ == "__main__":
    main()
