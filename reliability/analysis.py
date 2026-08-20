"""可复现性研究：评分者一致性分析。

用法：
    python reliability/analysis.py                      # A vs B
    python reliability/analysis.py rater_a rater_b2     # 任意两评分者
    python reliability/analysis.py rater_b rater_b2     # 轮次漂移
输入：ratings/<name>.json
输出：控制台报告 + ratings/agreement_report_<a>_<b>.json
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def normalize_level(raw):
    """把等级字符串规范化为有序集合。'L4+L0陈述层' -> frozenset({'L0','L4'})。"""
    if raw is None:
        return None
    s = str(raw).strip()
    if s.upper() in ("N/A", "NA", "非验证", "不适用"):
        return frozenset({"N/A"})
    if "理论" in s:
        return frozenset({"理论"})
    parts = re.split(r"[/+、,，]", s)
    lv = set()
    for p in parts:
        p = p.strip()
        m = re.search(r"L\s*\d", p)
        if m:
            lv.add(m.group(0).replace(" ", "").upper())
    if not lv:
        return frozenset({s})
    return frozenset(lv)


def load_ratings(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    out = {}
    for iid, r in d["ratings"].items():
        out[iid] = {"raw": r["level"], "norm": normalize_level(r["level"]),
                    "conf": r.get("confidence")}
    return out, d.get("rater")


LV_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
SPECIAL = {"N/A": 10, "理论": 11, "其他": 12}


def weakest(norm):
    """等级集合的最弱锚（论文规定报告等级=最弱锚）。N/A/理论 单独编码为可排序整数。"""
    if norm is None:
        return None
    if "N/A" in norm and len(norm) == 1:
        return SPECIAL["N/A"]
    if "理论" in norm and len(norm) == 1:
        return SPECIAL["理论"]
    lvs = [LV_ORDER[x] for x in norm if x in LV_ORDER]
    if not lvs:
        return SPECIAL["其他"]
    return min(lvs)


def cohen_kappa(a, b, labels):
    """简单 Cohen's kappa（名义类别）。a/b: dict item_id -> label。"""
    n = len(a)
    if n == 0:
        return None
    # 观察一致率
    po = sum(1 for i in a if a[i] == b[i]) / n
    # 期望一致率（按类别边际）
    pe = 0.0
    for lab in labels:
        pa = sum(1 for i in a if a[i] == lab) / n
        pb = sum(1 for i in b if b[i] == lab) / n
        pe += pa * pb
    if pe == 1.0:
        return 1.0 if po == 1.0 else None
    return (po - pe) / (1 - pe)


def main():
    names = sys.argv[1:3] if len(sys.argv) > 1 else ["rater_a", "rater_b"]
    if len(names) < 2:
        names = [names[0], "rater_b"]
    a, a_name = load_ratings(os.path.join(HERE, "ratings", names[0] + ".json"))
    b, b_name = load_ratings(os.path.join(HERE, "ratings", names[1] + ".json"))
    if not b:
        print(f"ratings/{names[1]}.json 不存在或为空。")
        return

    overlap = sorted(set(a) & set(b))
    labels = sorted({a[i]["norm"] for i in overlap} | {b[i]["norm"] for i in overlap})

    exact = {i: (a[i]["norm"] == b[i]["norm"]) for i in overlap}
    agree = sum(exact.values())
    n = len(overlap)
    pct = agree / n * 100 if n else 0.0
    kappa = cohen_kappa({i: a[i]["norm"] for i in overlap},
                        {i: b[i]["norm"] for i in overlap}, labels)

    # 最弱锚一致性（论文规定报告等级=判定路径最弱锚）
    wa = {i: weakest(a[i]["norm"]) for i in overlap}
    wb = {i: weakest(b[i]["norm"]) for i in overlap}
    wa_exact = {i: (wa[i] == wb[i]) for i in overlap}
    wa_agree = sum(wa_exact.values())
    wa_pct = wa_agree / n * 100 if n else 0.0
    wa_labels = sorted({wa[i] for i in overlap} | {wb[i] for i in overlap})
    wa_kappa = cohen_kappa(wa, wb, wa_labels)

    # 类别
    with open(os.path.join(HERE, "corpus.json"), encoding="utf-8") as f:
        corpus = json.load(f)
    cat = {it["id"]: it["category"] for it in corpus["items"]}
    cats = sorted({cat.get(i, "?") for i in overlap})

    print(f"== 一致性报告: {a_name} vs {b_name} ==")
    print(f"重叠条目: {n} / 48")
    print(f"等级精确一致率: {agree}/{n} = {pct:.1f}%")
    print(f"Cohen's kappa: {kappa:.3f}" if kappa is not None else "Cohen's kappa: N/A")
    print(f"最弱锚一致率: {wa_agree}/{n} = {wa_pct:.1f}%  (kappa={wa_kappa:.3f})")
    print()
    for c in cats:
        ids = [i for i in overlap if cat.get(i) == c]
        if not ids:
            continue
        ca = sum(exact[i] for i in ids)
        print(f"  [{c}] {ca}/{len(ids)} = {ca/len(ids)*100:.1f}% 一致")
    print()
    print("== 分歧清单 ==")
    for i in overlap:
        if not exact[i]:
            print(f"  {i}: A={a[i]['raw']} ({sorted(a[i]['norm'])})  vs  "
                  f"B={b[i]['raw']} ({sorted(b[i]['norm'])})")

    report = {
        "rater_a": a_name, "rater_b": b_name,
        "overlap": n, "agree_count": agree, "agree_pct": round(pct, 1),
        "kappa": round(kappa, 3) if kappa is not None else None,
        "weakest_agree_pct": round(wa_pct, 1),
        "weakest_kappa": round(wa_kappa, 3) if wa_kappa is not None else None,
        "per_category": {c: {"agree": sum(exact[i] for i in [x for x in overlap if cat.get(x) == c]),
                             "total": len([x for x in overlap if cat.get(x) == c])} for c in cats},
        "disagreements": [{"id": i, "A": a[i]["raw"], "B": b[i]["raw"],
                           "A_norm": sorted(a[i]["norm"]), "B_norm": sorted(b[i]["norm"])}
                          for i in overlap if not exact[i]],
    }
    with open(os.path.join(HERE, "ratings", f"agreement_report_{names[0]}_{names[1]}.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n已写 ratings/agreement_report_{names[0]}_{names[1]}.json")


if __name__ == "__main__":
    main()
