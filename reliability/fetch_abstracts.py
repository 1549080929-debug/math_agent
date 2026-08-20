"""P3 验证数据收集 v2：用 arXiv export API 抓取摘要（Atom XML 解析，可靠）。

用法：python reliability/fetch_abstracts.py
结果存 reliability/validation/abstracts/。
"""
import io
import json
import os
import re
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "validation", "abstracts")
os.makedirs(OUT, exist_ok=True)

ID_LIST = {
    "N28": "2310.10501",   # NeMo Guardrails
    "N29": "2503.18813",   # CaMeL (Defeating Prompt Injections by Design)
    "N30": "2504.11703",   # Progent
    "N31": "2505.23643",   # IFC
    "N32": "2510.02373",   # A-MemGuard
    "N33": "2210.08726",   # RARR
}


def get(url, t=25):
    req = urllib.request.Request(url, headers={"User-Agent": "research-yajie"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_entries(xml):
    out = {}
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        idm = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e)
        tm = re.search(r"<title>(.*?)</title>", e, re.S)
        sm = re.search(r"<summary>(.*?)</summary>", e, re.S)
        aid = idm.group(1) if idm else "?"
        aid = re.sub(r"v\d+$", "", aid)  # 去掉版本后缀：2310.10501v1 -> 2310.10501
        out[aid] = {
            "title": re.sub(r"\s+", " ", tm.group(1)).strip() if tm else "?",
            "abstract": re.sub(r"\s+", " ", sm.group(1)).strip() if sm else "?",
        }
    return out


def main():
    ids = ",".join(ID_LIST.values())
    xml = get(f"http://export.arxiv.org/api/query?id_list={ids}&max_results=10")
    parsed = parse_entries(xml)
    results = {}
    for cid, aid in ID_LIST.items():
        if aid in parsed:
            results[cid] = {"arxiv_id": aid, **parsed[aid]}
            print(f"[{cid}] {aid} | {parsed[aid]['title'][:70]}")
            print(f"    {parsed[aid]['abstract'][:160]}...")
        else:
            print(f"[{cid}] {aid} NOT FOUND in API response")

    # 搜 SafeAgent 正确 ID
    q = urllib.parse.quote('ti:"SafeAgent"')
    xml2 = get(f"http://export.arxiv.org/api/query?search_query={q}&max_results=5")
    safe = parse_entries(xml2)
    print("\n=== SafeAgent 搜索结果 ===")
    for aid, info in safe.items():
        print(f"  {aid} | {info['title'][:70]}")
    if safe:
        results["N41"] = {"arxiv_id": next(iter(safe)), **next(iter(safe.values()))}

    with io.open(os.path.join(OUT, "_api_summary.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n已存 {len(results)} 个摘要")


if __name__ == "__main__":
    main()
