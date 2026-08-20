"""调试 arXiv API：id_list 原始响应 + SafeAgent 精确搜索。"""
import re
import urllib.parse
import urllib.request


def get(url, t=25):
    req = urllib.request.Request(url, headers={"User-Agent": "research-yajie"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", errors="replace")


def main():
    raw = get("http://export.arxiv.org/api/query?id_list=2310.10501&max_results=1")
    print("RAW len:", len(raw))
    print(raw[:800])
    print("---")

    for qstr in ['all:"safe action" AND all:"LLM agents"',
                 'ti:"SafeAgent" AND abs:"plan" AND abs:"tool"']:
        q = urllib.parse.quote(qstr)
        xml = get("http://export.arxiv.org/api/query?search_query=" + q + "&max_results=8")
        print(f"== {qstr} ==")
        for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
            idm = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e)
            tm = re.search(r"<title>(.*?)</title>", e, re.S)
            sm = re.search(r"<summary>(.*?)</summary>", e, re.S)
            title = re.sub(r"\s+", " ", tm.group(1)).strip() if tm else "?"
            summ = re.sub(r"\s+", " ", sm.group(1)).strip() if sm else "?"
            print("HIT:", idm.group(1) if idm else "?", "|", title[:80])
            print("    ", summ[:200])


if __name__ == "__main__":
    main()
