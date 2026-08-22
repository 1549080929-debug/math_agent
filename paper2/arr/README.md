# ARR 投稿管线（The Same Zero → ACL 格式 PDF）

> 用途：把 `paper_arr.md`（ARR 压缩版，正文 8 页）构建为 ACL 投稿格式 PDF。
> 一条命令：`python paper2/arr/rebuild_full.py`

## 文件结构

| 文件 | 作用 |
|---|---|
| `paper_arr.md` | **ARR 压缩版源**（完整版在 `paper2/paper.md`，勿改） |
| `refs.bib` | 15 条参考文献（BibTeX） |
| `chicago-author-date.csl` | 引用样式（作者-年份） |
| `acl.sty` / `acl_latex.tex` / `acl_natbib.bst` | ACL 官方模板 |
| `rebuild_full.py` | **主管线**（一条命令完成全部） |
| `build_arr.py` | ACL preamble + 正文组装（含动态 CSL 提取） |
| `fix_latex.py` | Unicode 转义 + longtable → table*（tabularx 等分列，总宽 \textwidth） |
| `fix_format.py` | 章节编号去重 + Appendix → section* |
| `fix_natbib3.py` | 参考文献 → enumerate（绕开 natbib） |
| `acl_submit.tex` | 生成的 LaTeX（管线跑完自动归档 `archive/arr_intermediates/`） |
| `acl_submit.pdf` | **投稿 PDF**（正文 8 页 + 附录 + 参考文献） |
| `archive/arr_versions/` | 版本存档（v12 压缩前 + scripts_compression + anon_prep_20260822，已移出主目录） |

## 管线步骤（rebuild_full.py 自动执行）

```
paper_arr.md
  → map citations（[n] → [@key]）
  → pandoc（citeproc + wrap=none）→ paper_arr.tex
  → build_arr.py（ACL 模板 + CSL 定义）→ acl_submit.tex
  → fix_latex.py（Unicode + longtable→table*）
  → fix_format.py（编号去重 + Appendix）
  → fix_natbib3.py（References→enumerate）
  → xelatex → acl_submit.pdf
```

## 关键纪律

1. **改 paper_arr.md 后必须重跑 rebuild_full.py**（全管线），不能只跑下游——否则下游产物 stale
2. **完整版（paper2/paper.md）不动**——ARR 压缩只在 paper_arr.md
3. 版本存档：压缩前版本在 `archive/arr_versions/v12_body10p_20260822/`
4. 修复轨迹脚本在 `archive/arr_versions/scripts_compression/`（可重放每步压缩）

## 已知边界

- natbib 警告（参考文献转 enumerate 后 acl.sty 的 natbib 风格提示）——不影响 PDF 内容
- Appendix 编号为 section*（不编号），A.1/A.2/A.4 手动编号
- 表格为 tabularx（总宽 = \textwidth，内容自动换行，2026-08-22 修复：原 l 列 + minipage{\linewidth} 导致全部表格 Overfull 超宽 946–2348pt、溢出页面右边界；Level map 表首列为 p{1.2cm} 窄列，其余 X 等分——不能用 l/c 列，l/c 中 minipage{\linewidth}=\textwidth 会把 X 列挤成 0）

## 环境

- pandoc 3.9（pypandoc-binary）
- TinyTeX（C:\TinyTeX，ASCII 路径——中文路径 kpathsea 不支持）
- xelatex（Unicode 原生；pdflatex 不支持 α/κ）
