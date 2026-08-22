"""Update HANDOFF.md to v5."""
import io

path = 'HANDOFF.md'
s = io.open(path, encoding='utf-8').read()

old = '> 最后更新：2026-08-22（v4）。v3 交接于同日（覆盖 Z(α)/funnel/JADE/LITMUS/方法论宣言），本版新增：C1a 完成、arXiv 退回、ARR 投稿管线（8 页版就绪）。'
new = ('> 最后更新：2026-08-22（v5）。v4 交接于同日（C1a/arXiv 退回/ARR 管线）；本版新增：**ARR 周期修正（10-12 提交，非 12 月）、'
       '匿名化投稿 PDF 就绪、表单材料包（submission_form.md）、ARR 官方要求核实（页数/匿名/checklist/Limitations 硬性）**。')
assert old in s, 'header'
s = s.replace(old, new)

old2 = '| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回（08-20 老版本）**——arXiv moderation 判定需正式同行评审；appeal 需期刊 DOI。**决定：投 ARR 2026-12 → ACL 2027**（docs/17 规划） |'
new2 = '| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回**；**ARR October 2026 周期（10-12 提交）→ ACL 2027**。匿名化 PDF + 表单材料包就绪（v5） |'
assert old2 in s, 'paper table'
s = s.replace(old2, new2)

old3 = '**下一步（ARR）**：提交表单（title/abstract ≤200 words/comments/分类 cs.CL 主）、可能需再打磨 natbib 警告（可接受）、ARR 2026-12 提交。'
new3 = ('**下一步（ARR）**：见 `paper2/arr/submission_form.md`（权威材料包：title/199 词 abstract/comments/track=LLM agents/checklist 草稿/开放问题）。'
        '⚠️ **周期修正**：ARR 无 12 月周期（10 周一轮）；最近窗口 = **2026-10-12（October 2026）→ meta-review 12-20 → 2027-01 承诺 ACL 2027**。'
        '匿名化已做（build_arr.py \\author Anonymous + paper_arr.md 去身份块 + refs.bib 自引匿名 + 摘要去 arXiv 号；命名版备份 versions/anon_prep_20260822/）。')
assert old3 in s, '下一步'
s = s.replace(old3, new3)

old4 = '| `paper2/arr/` | ARR 管线（README.md 是入口）|'
new4 = '| `paper2/arr/` | ARR 管线（README.md 入口）；**`submission_form.md` = 提交表单材料包（权威）**；`versions/anon_prep_20260822/` = 匿名化前命名版备份 |'
assert old4 in s, 'file index'
s = s.replace(old4, new4)

io.open(path, 'w', encoding='utf-8', newline='').write(s)
print('HANDOFF.md updated to v5')
