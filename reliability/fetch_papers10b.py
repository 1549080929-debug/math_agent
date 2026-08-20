"""补抓 P02（arXiv 搜索 test oracle / source of authority）与 P08（preprints.org 带 headers）。"""
import io
import json
import os
import re
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "validation", "papers10")


def get(url, t=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", errors="replace")


def main():
    extra = {}

    # P08 preprints.org
    try:
        html = get("https://www.preprints.org/manuscript/202601.0892")
        text = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        extra["P08"] = {"source": "preprints.org 202601.0892", "title": "(网页)", "abstract": text[:4000]}
        print("P08 OK len=%d" % len(text))
        print(text[:350])
    except Exception as e:
        print("P08 FAILED:", e)

    # P02 搜索（多种查询）
    for qstr in ['all:"test oracle" AND all:"source of authority"',
                 'all:"test oracles" AND all:"taxonomy" AND all:"LLM"',
                 'ti:"source of authority"']:
        q = urllib.parse.quote(qstr)
        try:
            xml = get("http://export.arxiv.org/api/query?search_query=" + q + "&max_results=6")
            hits = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
            print(f"\n== {qstr} ({len(hits)} hits) ==")
            for e in hits:
                idm = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e)
                tm = re.search(r"<title>(.*?)</title>", e, re.S)
                title = re.sub(r"\s+", " ", tm.group(1)).strip() if tm else "?"
                aid = re.sub(r"v\d+$", "", idm.group(1)) if idm else "?"
                print("HIT:", aid, "|", title[:85])
                if "oracle" in title.lower() or "authority" in title.lower():
                    sm = re.search(r"<summary>(.*?)</summary>", e, re.S)
                    summ = re.sub(r"\s+", " ", sm.group(1)).strip() if sm else "?"
                    extra["P02"] = {"source": f"arXiv:{aid}", "title": title, "abstract": summ}
        except Exception as e:
            print(f"search FAILED: {e}")

    with io.open(os.path.join(OUT, "_papers10b.json"), "w", encoding="utf-8") as f:
        json.dump(extra, f, ensure_ascii=False, indent=2)
    print("\n已存补充结果")


if __name__ == "__main__":
    main()
