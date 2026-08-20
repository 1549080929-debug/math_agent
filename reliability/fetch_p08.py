"""搜 P08（Limits of Self-Correction / correlated errors）的 arXiv 版本 + 读已存的 P02 摘要。"""
import io
import json
import os
import re
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def get(url, t=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", errors="replace")


def main():
    # 读已存 P02
    with io.open(os.path.join(HERE, "validation", "papers10", "_papers10b.json"), encoding="utf-8") as f:
        b = json.load(f)
    if "P02" in b:
        print("=== P02 (arXiv:2607.05031) 摘要 ===")
        print(b["P02"]["abstract"])
        print()

    # 搜 P08
    for qstr in ['ti:"Limits of Self-Correction"',
                 'all:"self-correction" AND all:"correlated errors"']:
        q = urllib.parse.quote(qstr)
        try:
            xml = get("http://export.arxiv.org/api/query?search_query=" + q + "&max_results=6")
            print(f"== {qstr} ==")
            for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
                idm = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e)
                tm = re.search(r"<title>(.*?)</title>", e, re.S)
                title = re.sub(r"\s+", " ", tm.group(1)).strip() if tm else "?"
                aid = re.sub(r"v\d+$", "", idm.group(1)) if idm else "?"
                print("HIT:", aid, "|", title[:85])
                sm = re.search(r"<summary>(.*?)</summary>", e, re.S)
                if "Self-Correction" in title:
                    summ = re.sub(r"\s+", " ", sm.group(1)).strip() if sm else "?"
                    print("   摘要:", summ[:400])
        except Exception as ex:
            print(f"search FAILED: {ex}")
        print()


if __name__ == "__main__":
    main()
