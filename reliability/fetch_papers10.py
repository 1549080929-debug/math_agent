"""抓取 10 篇文献的摘要（arXiv API + 直接 curl 非 arXiv 源）。

用法：python reliability/fetch_papers10.py
结果：reliability/validation/papers10/（每篇 title+abstract）
"""
import io
import json
import os
import re
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "validation", "papers10")
os.makedirs(OUT, exist_ok=True)

ARXIV_IDS = {
    "P01": "2605.08442",   # Defense Effectiveness Across Architectural Layers
    "P03": "2604.02617",   # AutoVerifier
    "P04": "2606.02289",   # DECK taxonomy
    "P05": "2602.13224",   # Geometric Taxonomy of Hallucination
    "P06": "2511.15759",   # Securing AI Agents Against Prompt Injection
    "P07": "2512.02304",   # When Does Verification Pay Off
    "P09": "2607.29167",   # PPMF（已深读，仅存档）
    "P10": "2504.00406",   # VerifiAgent（已深读，仅存档）
}

NON_ARXIV = {
    "P02": "https://themoolight.io/",
    "P08": "https://www.preprints.org/manuscript/202601.0892",
}


def get(url, t=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", errors="replace")


def main():
    results = {}

    # arXiv 批量
    ids = ",".join(ARXIV_IDS.values())
    xml = get(f"http://export.arxiv.org/api/query?id_list={ids}&max_results=20")
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        idm = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e)
        tm = re.search(r"<title>(.*?)</title>", e, re.S)
        sm = re.search(r"<summary>(.*?)</summary>", e, re.S)
        aid = re.sub(r"v\d+$", "", idm.group(1)) if idm else "?"
        title = re.sub(r"\s+", " ", tm.group(1)).strip() if tm else "?"
        abstract = re.sub(r"\s+", " ", sm.group(1)).strip() if sm else "?"
        for key, want in ARXIV_IDS.items():
            if aid == want:
                results[key] = {"source": f"arXiv:{aid}", "title": title, "abstract": abstract}
                print(f"[{key}] {aid} | {title[:75]}")
                print(f"    {abstract[:150]}...")

    # 非 arXiv（直接抓网页文本）
    for key, url in NON_ARXIV.items():
        try:
            html = get(url)
            text = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text)
            results[key] = {"source": url, "title": "(网页)", "abstract": text[:3000]}
            print(f"[{key}] {url} | 抓取 {len(text)} 字符")
            print(f"    {text[:150]}...")
        except Exception as ex:
            print(f"[{key}] {url} FAILED: {ex}")

    with io.open(os.path.join(OUT, "_papers10.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n已存 {len(results)} 篇 → {OUT}")


if __name__ == "__main__":
    main()
