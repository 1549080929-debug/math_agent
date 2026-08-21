"""构建工具：paper2/paper.md -> paper2/paper.html -> paper2/paper.pdf (Edge 无头)。

用法：python paper2/build_paper2.py
依赖：pip install markdown；本机装有 Microsoft Edge。
"""
import os
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "paper.md")
OUT_HTML = os.path.join(HERE, "paper.html")
OUT_PDF = os.path.join(HERE, "paper.pdf")

CSS = """
<style>
  body { font-family: "Georgia", "Times New Roman", serif; font-size: 11pt;
         line-height: 1.55; max-width: 46em; margin: 0 auto; padding: 2em; color: #111; }
  h1 { font-size: 17pt; text-align: center; margin-bottom: 0.2em; }
  h2 { font-size: 13.5pt; border-bottom: 1px solid #ccc; padding-bottom: 2px; margin-top: 1.6em; }
  h3 { font-size: 12pt; margin-top: 1.2em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 9.5pt; }
  th, td { border: 1px solid #999; padding: 4px 6px; text-align: left; vertical-align: top; }
  th { background: #f0f0f0; }
  pre { background: #f6f6f6; border: 1px solid #ddd; padding: 8px; font-size: 8.5pt;
        white-space: pre; overflow-x: auto; }
  code { font-family: Consolas, monospace; font-size: 9pt; }
  blockquote { border-left: 3px solid #bbb; margin-left: 0; padding-left: 1em; color: #333; }
  em { font-style: italic; }
  @media print { body { padding: 0; } h2 { page-break-after: avoid; } table, pre { page-break-inside: avoid; } }
</style>
"""


def main():
    raw = open(SRC, encoding="utf-8").read()
    body = markdown.markdown(raw, extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
    html = f'<!DOCTYPE html><html><head><meta charset="utf-8">{CSS}</head><body>{body}</body></html>'
    open(OUT_HTML, "w", encoding="utf-8").write(html)
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        print("Edge not found; HTML written but PDF skipped:", OUT_HTML)
        return 1
    uri = "file:///" + OUT_HTML.replace("\\", "/")
    subprocess.run([edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", uri], check=True, capture_output=True)
    print("written:", OUT_HTML, OUT_PDF)
    return 0


if __name__ == "__main__":
    sys.exit(main())
