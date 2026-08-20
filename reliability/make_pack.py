"""可复现性研究：生成 Rater A 答案 + Rater B 盲评证据包。

用法：python reliability/make_pack.py
产出：
  ratings/rater_a.json     作者判级（corpus.json 中 author_level 非空者）
  evidence_pack.json       Rater B 盲评用（剥掉一切判级结论，清理带暗示的证据）
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# 证据清理：把结论性措辞换成纯机制描述（防盲评污染）
CLEAN = {
    "S03": ["端点+驻点穷举（对二次函数区间问题）"],
    "S08": ["类型系统：校验答案的类型符合声明类型"],
    "L16": ["对象是模型自评（自验证）现象的理论形式化", "无运行时判定"],
}


def main():
    with open(os.path.join(HERE, "corpus.json"), encoding="utf-8") as f:
        corpus = json.load(f)

    os.makedirs(os.path.join(HERE, "ratings"), exist_ok=True)

    # ---- Rater A（作者判级）----
    rater_a = {
        "rater": "A (author)",
        "source": "docs/07 (lit17) + docs/06 §7 (sys)",
        "ratings": {}
    }
    for it in corpus["items"]:
        if not it["pending_author"] and it["author_level"] is not None:
            rater_a["ratings"][it["id"]] = {
                "level": it["author_level"],
                "confidence": it["author_confidence"],
            }
    with open(os.path.join(HERE, "ratings", "rater_a.json"), "w", encoding="utf-8") as f:
        json.dump(rater_a, f, ensure_ascii=False, indent=2)

    # ---- Rater B 证据包（无答案）----
    pack = {
        "study": corpus["study"],
        "protocol": "protocol_v2.md",
        "instruction": "仅依据每条目的 mechanism/evidence 判级；证据不足标 CONF=low 并按现有证据判；不要参考任何其他文件。",
        "items": []
    }
    for it in corpus["items"]:
        evidence = CLEAN.get(it["id"], it["evidence"])
        pack["items"].append({
            "id": it["id"],
            "name": it["name"],
            "category": it["category"],
            "source": it["source"],
            "mechanism": it["mechanism"],
            "evidence": evidence,
        })
    with open(os.path.join(HERE, "evidence_pack.json"), "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)

    n_a = len(rater_a["ratings"])
    print(f"rater_a: {n_a} items | evidence_pack: {len(pack['items'])} items")


if __name__ == "__main__":
    main()
