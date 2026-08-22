"""Fix STATUS.md updates (line-anchored)."""
import io

path = 'STATUS.md'
s = io.open(path, encoding='utf-8').read()

lines = s.split('\n')
out = []
for ln in lines:
    if ln.startswith('1. **第二篇论文投稿**'):
        out.append('1. **第二篇论文投稿（ARR October 2026 周期，10-12 截止）**：✅ 匿名化投稿 PDF 就绪（无作者/邮箱/ORCID/GitHub/自引 arXiv 号，pypdf 全文扫描 clean）+ 表单材料包就绪（`paper2/arr/submission_form.md`：title/199 词 abstract/comments/track=LLM agents/checklist 草稿）。**待用户操作**：① 注册 OpenReview + 完善 profile（affiliation/semantic scholar/dblp/anthology）② 提交后 48h 内所有作者注册 reviewer ③ 决定 preprint binding 选项 ④ aclpubcheck 过稿 + acl.sty 对照官方最新模板 ⑤ 可选增强：C1 另一半（bounded exception）。⚠️ 周期修正：ARR 无 12 月周期（10 周一轮），最近窗口 2026-10-12')
    elif '② The Same Zero' in ln:
        out.append('- **论文**：① arXiv:2608.19009（v2 已公布）· ② The Same Zero（paper2/，arXiv 退回；ARR October 2026 周期投稿准备中，匿名化 PDF + 表单材料包就绪）')
    else:
        out.append(ln)

io.open(path, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('STATUS.md updated')
