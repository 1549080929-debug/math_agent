"""专著装配：docs/01-15 + RESULTS/REPORT + 论文 → 一本 PDF 书。

用法：python book/build_book.py
产出：book/book.html → book/book.pdf（Edge 无头打印，同 build_pdf.py 管线）
"""
import os
import re
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FRONT = os.path.join(HERE, "00-封面与序言.md")
OUT_HTML = os.path.join(HERE, "book.html")
OUT_PDF = os.path.join(HERE, "book.pdf")

# (部, [(章号, 相对路径)])
PARTS = [
    ("第一部 · 主线", [
        (1, "docs/01-研究叙事.md"),
        (2, "docs/02-失败模式分类学.md"),
    ]),
    ("第二部 · 四章实证", [
        (3, "docs/03-架构设计备忘.md"),
        (4, "docs/04-实验档案.md"),
        (5, "RESULTS.md"),
        (6, "behavior/REPORT.md"),
        (7, "medical/REPORT.md"),
        (8, "docs/08-第四章-代码生成验证.md"),
    ]),
    ("第三部 · VAL 框架", [
        (9, "docs/05-锚定层级.md"),
        (10, "docs/06-判级标准.md"),
        (11, "docs/07-文献评述.md"),
        (12, "docs/09-抬级器可行性.md"),
        (13, "docs/10-对抗性评审答辩.md"),
    ]),
    ("第四部 · 裁判的裁判", [
        (14, "docs/11-判级可复现性研究.md"),
        (15, "docs/13-锚语义类型学.md"),
    ]),
    ("第五部 · Agent 安全（方向 3）", [
        (16, "docs/12-VAL×Agent安全：PPMF案例.md"),
        (17, "docs/14-VAL预测协议-Agent安全.md"),
        (18, "docs/15-方向3综合：VAL预测安全防御.md"),
        (19, "docs/23-论文2定位与Agent安全证据链.md"),
    ]),
    ("第六部 · 收束", [
        (20, "EVALUATION.md"),
        (21, "paper/preprint.md"),
        (22, "docs/24-方法论宣言.md"),
    ]),
]

APPENDIX = [
    ("附录 A", "README.md"),
    ("附录 B", "HANDOFF.md"),
    ("附录 C", "docs/验证栈审计报告.md"),
]


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def strip_mermaid(text):
    return re.sub(r"```mermaid.*?```", "", text, flags=re.S)


def demote_headers(text):
    """把文档标题降一级（h1→h2），避免与章节 h1 冲突；代码块内的 # 不动。"""
    out = []
    in_fence = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence and line.startswith("#"):
            out.append("#" + line)
        else:
            out.append(line)
    return "\n".join(out)


def fix_img_src(text, chapter_path):
    """把章节内的相对图片路径改成从 book/ 出发的路径。"""
    base = os.path.dirname(chapter_path)
    if not base:
        return text
    return re.sub(r'src="([^"]+)"',
                  lambda m: f'src="{os.path.join(base, m.group(1)).replace(os.sep, "/")}"',
                  text)


def assemble():
    chunks = []
    chunks.append(strip_comments(open(FRONT, encoding="utf-8").read()))

    for part, chapters in PARTS:
        chunks.append(f"\n\n<div class=\"part\">{part}</div>\n\n")
        for num, path in chapters:
            full = os.path.join(ROOT, path)
            raw = open(full, encoding="utf-8").read()
            raw = strip_comments(strip_mermaid(raw))
            raw = demote_headers(raw)
            raw = fix_img_src(raw, path)
            chunks.append(f"\n\n<div class=\"chapter\">第 {num} 章</div>\n\n{raw}\n\n")

    # 附录
    chunks.append("\n\n<div class=\"part\">附录</div>\n\n")
    for label, path in APPENDIX:
        full = os.path.join(ROOT, path)
        raw = open(full, encoding="utf-8").read()
        raw = strip_comments(strip_mermaid(raw))
        raw = demote_headers(raw)
        raw = fix_img_src(raw, path)
        chunks.append(f"\n\n<div class=\"chapter\">{label}</div>\n\n{raw}\n\n")

    return "\n".join(chunks)


CSS = """
<style>
  body { font-family: "Georgia", "Times New Roman", "Microsoft YaHei", serif; font-size: 10.5pt;
         line-height: 1.65; max-width: 44em; margin: 0 auto; padding: 2em; color: #111; }
  h1 { font-size: 20pt; text-align: center; margin: 0.4em 0; }
  h2 { font-size: 14pt; border-bottom: 1px solid #bbb; padding-bottom: 2px; margin-top: 1.8em; page-break-after: avoid; }
  h3 { font-size: 12pt; margin-top: 1.4em; }
  h4 { font-size: 11pt; margin-top: 1.1em; }
  .part { page-break-before: always; text-align: center; font-size: 17pt; font-weight: bold;
          border-top: 2px solid #333; border-bottom: 2px solid #333; padding: 1.2em 0; margin: 3em 0; }
  .chapter { page-break-before: always; font-size: 15pt; font-weight: bold; color: #1a4d8f;
             border-bottom: 3px solid #1a4d8f; padding-bottom: 4px; margin-top: 2em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 9pt; }
  th, td { border: 1px solid #999; padding: 3px 5px; text-align: left; vertical-align: top; }
  th { background: #f0f0f0; }
  pre { background: #f6f6f6; border: 1px solid #ddd; padding: 7px; font-size: 8pt;
        white-space: pre; overflow-x: auto; }
  code { font-family: Consolas, monospace; font-size: 8.5pt; }
  blockquote { border-left: 3px solid #bbb; margin-left: 0; padding-left: 1em; color: #333; }
  img { max-width: 100%; }
  em { font-style: italic; }
  @media print { body { padding: 0; } h2, h3 { page-break-after: avoid; } table, pre { page-break-inside: avoid; } }
</style>
"""


def main():
    body = assemble()
    html = f'<!DOCTYPE html><html><head><meta charset="utf-8">{CSS}</head><body>{markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists", "nl2br"])}</body></html>'
    open(OUT_HTML, "w", encoding="utf-8").write(html)

    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        print("Edge not found; HTML written but PDF skipped:", OUT_HTML)
        return 1
    uri = "file:///" + OUT_HTML.replace("\\", "/")
    subprocess.run([edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", uri],
                   check=True, capture_output=True)
    print("written:", OUT_HTML, OUT_PDF)
    return 0


if __name__ == "__main__":
    sys.exit(main())
