"""Update docs/17, STATUS.md, HANDOFF.md with verified ARR cycle + submission prep status."""
import io

def rw(path, fn):
    raw = io.open(path, 'rb').read()
    crlf = b'\r\n' in raw
    s = raw.decode('utf-8')
    s = fn(s)
    out = s.replace('\r\n', '\n')
    if crlf:
        out = out.replace('\n', '\r\n')
    io.open(path, 'w', encoding='utf-8', newline='').write(out)
    print('updated:', path)

# ---------- docs/17 ----------
def d17(s):
    old = '> \u26a0\ufe0f 日期为常规周期推断（ARR 滚动制 + 会议惯例），**投稿前用官方 CFP 核实**。'
    new = ('> \u26a0\ufe0f **2026-08-22 官方核实（aclrollingreview.org/dates）**：ARR 自 2025-05 起为 **10 周一轮（一年 5 轮）**，'
           '不存在"12 月周期"。2026 各轮提交：Mar 16 / May 25 / Aug 3（已过）/ **Oct 12** / 下一轮 TBA（约 12 月-1 月）。\n'
           '> **修订：投 October 2026 周期（提交 2026-10-12，meta-review 2026-12-20），2027-01 承诺 ACL 2027。** '
           '详情见 `paper2/arr/submission_form.md`（权威版）。')
    assert old in s, 'd17 banner'
    s = s.replace(old, new)
    old2 = '**推荐节奏**：现在→11 月增强 → 12 月投 ARR 第一轮（目标 ACL 2027）→ 2-3 月拿意见改稿 → 未中则 5-6 月 ARR 二轮（EMNLP 2027）→ workshop 兜底。'
    new2 = ('**推荐节奏（2026-08-22 修订）**：现在→10-12 前增强与打磨 → **10-12 投 ARR October 2026 周期** → 12-20 拿 meta-reviews → '
            '2027-01 承诺 ACL 2027 → 未中则下一轮 ARR（约 2027-02/03）→ EMNLP 2027 兜底。')
    assert old2 in s, 'd17 推荐节奏'
    s = s.replace(old2, new2)
    old3 = '| 2026-11 | 杠杆 2 完成 + 杠杆 3/4 收尾 | 论文 v2（paper2 修订）成稿 |\r\n| 2026-12 | **ARR 第一轮提交**（目标 ACL 2027） | 提交凭证 |\r\n| 2027-02~03 | ARR 意见 → 改稿 | 修订版 |\r\n| 2027-05~06 | 未中则 ARR 二轮（EMNLP 2027） | 提交凭证 |'
    new3 = ('| 2026-09-10 | 杠杆 1/3 收尾（可选）+ 表单材料定稿 | submission_form.md 全项就绪 |\r\n'
            '| **2026-10-12** | **ARR 提交（October 2026 周期）** | 提交凭证 |\r\n'
            '| 2026-12-20 | meta-reviews 发布 | 意见 → 改稿 |\r\n'
            '| 2027-01 | 承诺 ACL 2027 | 提交凭证 |\r\n'
            '| 2027 春 | 未中则 ARR 二轮（EMNLP 2027） | 提交凭证 |')
    assert old3 in s, 'd17 timeline'
    s = s.replace(old3, new3)
    return s

# ---------- STATUS.md ----------
def st(s):
    old = '| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回（08-20 老版本）**——arXiv moderation 判定需正式同行评审；appeal 需期刊 DOI。**决定：投 ARR 2026-12 → ACL 2027**（docs/17 规划） |'
    new = '| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回（08-20 老版本）**——arXiv moderation 判定需正式同行评审。**决定：投 ARR October 2026 周期（10-12 提交）→ ACL 2027**（docs/17 + paper2/arr/submission_form.md）；匿名化 PDF + 表单材料包已就绪（08-22） |'
    assert old in s, 'STATUS paper table'
    s = s.replace(old, new)
    old2 = '1. **第二篇论文投稿**：⚠️ **arXiv 退回（08-20 提交的老版本）**——arXiv 建议"找专业同行审批"（endorsement/分类问题待确认）。新版 The Same Zero（含 4 贡献 + Z(α)/funnel + 8 项边界收紧）已是投稿版。投稿点候选：ARR 2026-12 → ACL 2027 / EMNLP 2027（docs/17 已有规划）；CCS/USENIX（需补 threat model）；AAAI/Findings。**重新提交 arXiv 新版 vs 直接走正式投稿，待用户定夺**'
    new2 = ('1. **第二篇论文投稿（ARR October 2026 周期，10-12 截止）**：✅ 匿名化投稿 PDF 就绪（无作者/邮箱/ORCID/GitHub/自引 arXiv 号，pypdf 扫描 clean）+ '
            '表单材料包就绪（`paper2/arr/submission_form.md`：title/199 词 abstract/comments/track=LLM agents/checklist 草稿）。'
            '**待用户操作**：① 注册 OpenReview + 完善 profile（affiliation/semantic scholar/dblp/anthology）② 提交后 48h 内所有作者注册 reviewer '
            '③ 决定 preprint binding 选项 ④ aclpubcheck 过稿 + acl.sty 对照官方最新模板 ⑤ 可选：C1 另一半（bounded exception）作为增强')
    assert old2 in s, 'STATUS 待办1'
    s = s.replace(old2, new2)
    return s

# ---------- HANDOFF.md ----------
def hd(s):
    old = '> 最后更新：2026-08-22（v4）。v3 交接于同日（覆盖 Z(α)/funnel/JADE/LITMUS/方法论宣言），本版新增：C1a 完成、arXiv 退回、ARR 投稿管线（8 页版就绪）。'
    new = ('> 最后更新：2026-08-22（v5）。v4 交接于同日（C1a/arXiv 退回/ARR 管线）；本版新增：**ARR 周期修正（10-12 提交，非 12 月）、'
           '匿名化投稿 PDF 就绪、表单材料包（submission_form.md）、ARR 官方要求核实（页数/匿名/checklist/Limitations 硬性）**。')
    assert old in s, 'HANDOFF header'
    s = s.replace(old, new)
    old2 = '| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回（08-20 老版本）**——arXiv moderation 判定需正式同行评审；appeal 需期刊 DOI。**决定：投 ARR 2026-12 → ACL 2027**（docs/17 规划） |'
    new2 = '| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回**；**ARR October 2026 周期（10-12 提交）→ ACL 2027**。匿名化 PDF + 表单材料包就绪（v5） |'
    assert old2 in s, 'HANDOFF paper table'
    s = s.replace(old2, new2)
    old3 = '**下一步（ARR）**：提交表单（title/abstract ≤200 words/comments/分类 cs.CL 主）、可能需再打磨 natbib 警告（可接受）、ARR 2026-12 提交。'
    new3 = ('**下一步（ARR）**：见 `paper2/arr/submission_form.md`（权威材料包：title/199 词 abstract/comments/track=LLM agents/checklist 草稿/开放问题）。'
            '⚠️ **周期修正**：ARR 无 12 月周期（10 周一轮）；最近窗口 = **2026-10-12（October 2026）→ meta-review 12-20 → 2027-01 承诺 ACL 2027**。'
            '匿名化已做（build_arr.py \\author Anonymous + paper_arr.md 去身份块 + refs.bib 自引匿名；命名版备份在 versions/anon_prep_20260822/）。')
    assert old3 in s, 'HANDOFF 下一步'
    s = s.replace(old3, new3)
    old4 = '| `paper2/arr/` | ARR 管线（README.md 是入口）|'
    new4 = '| `paper2/arr/` | ARR 管线（README.md 入口）；**`submission_form.md` = 提交表单材料包（权威）**；`versions/anon_prep_20260822/` = 匿名化前命名版备份 |'
    assert old4 in s, 'HANDOFF file index'
    s = s.replace(old4, new4)
    return s

rw('docs/17-2027投稿规划.md', d17)
rw('STATUS.md', st)
rw('HANDOFF.md', hd)
print('ALL OK')
