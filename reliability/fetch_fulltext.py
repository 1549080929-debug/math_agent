"""抓取重点论文的 arXiv HTML 全文（前 8000 字符 + 分段存档）。

用法：python reliability/fetch_fulltext.py
结果：reliability/validation/papers10/fulltext/<id>.txt
"""
import io
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "validation", "papers10", "fulltext")
os.makedirs(OUT, exist_ok=True)

TARGETS = {
    "P01": "2605.08442",
    "P02": "2607.05031",
    "P07": "2512.02304",
}


def get(url, t=40):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_html(html):
    text = re.sub(r"<script.*?</script>|<style.*?</style>|math.*?</math>", "", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    return re.sub(r"[ \t]+", " ", text)


def main():
    for pid, aid in TARGETS.items():
        try:
            html = get(f"https://arxiv.org/html/{aid}")
            text = strip_html(html)
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            cleaned = "\n".join(lines)
            with io.open(os.path.join(OUT, f"{pid}.txt"), "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"[{pid}] {aid} OK, {len(cleaned)} 字符 → fulltext/{pid}.txt")
        except Exception as e:
            print(f"[{pid}] {aid} FAILED: {e}")


if __name__ == "__main__":
    main()
