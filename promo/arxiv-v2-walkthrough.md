# arXiv v2 提交走查（2608.19009 替换版）

> 准备：2026-08-20。PDF 已就绪：`paper/preprint.pdf`（21 页，v2 全量内容，含 arXiv ID 页脚）。
> 提交包：`paper/submission.md`（摘要/Comments 已同步 v2，AI 声明已补）。
> **状态：✅ 已完成**——v2 于 2026-08-20 公布：https://arxiv.org/abs/2608.19009v2（submit/7972294）。

---

## 步骤

1. 打开 https://arxiv.org/user/ → 登录（你提交 v1 的账号）
2. 在 dashboard 找到 2608.19009 → 点 **Submit a Replacement**（替换提交）
3. 逐项填表（见下方复制内容）：
   - **Title**：不变（ASCII 安全版）
   - **Authors**：不变（Yajie Yin）
   - **Abstract**：用 submission.md §3 的新版（含 "in our survey"）
   - **Comments**：用 v2 版（含修订说明 + AI 声明）
   - **Subject Category**：cs.CL 主类目不变（可选：v2 补加 cs.AI 交叉——在表单里加一行即可）
   - **License**：CC-BY 4.0 不变
   - **File**：上传 `paper/preprint.pdf`，文件格式选 **PDF only (no source)**
   - 五个可选字段（Report number / Journal ref / DOI / ACM / MSC）→ **全留空**（同 v1）
4. 预览检查：确认 21 页、Figure 1 正常渲染 → **Submit**
5. **点 arXiv 发来的验证邮件确认链接**（不点会卡 pending）
6. 等公布——替换版通常比首投快（几小时到 1 天），周日至周四 20:00 ET 公布

## 复制粘贴内容

**Abstract**（1857 字符，ASCII 安全，≤1920）：
复制 `paper/abstract_v2.txt` 全文（或 `paper/submission.md` §3 修正版）。含 "in our survey"。

**Comments（v2）**：
```
v2: added an inter-rater reproducibility study of the decision procedure (kappa~0.8 across four blind raters on 54-70 schemes), an agent-security case study (memory provenance laundering, PPMF), and anchor semantics (intent/truth/effect); 15+ fixes from a cold-eye review (numbers, citations, internal consistency).

Code and data: https://github.com/1549080929-debug/math_agent
Keywords: LLM verification; verification autonomy; completeness; ground truth; trustworthy AI
Writing and implementation assisted by an AI language model; all experiments, data, and research decisions are the author's own.
```

## 提交后

- 状态：Submitted → 验证邮件 → moderation → 公布（2508.19009v2）
- 公布后更新 README 状态（可选：v2 链接）
- 论文页脚的 arXiv:2608.19009 已就位（v2 起显示 2608.19009v2）
