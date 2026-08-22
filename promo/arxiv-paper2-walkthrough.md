# arXiv 投稿走查：第二篇 The Same Zero

> 准备：2026-08-20。PDF：`paper2/paper.pdf`（12 页，已验证）。
> 提交包：`paper2/submission.md`（摘要 1712 字符 ASCII 安全 · Comments 273 字符）。

---

## 步骤

1. 打开 https://arxiv.org/submit/ → 登录（同第一篇账号）
2. **Start new submission**，逐项填：
   - **Title**：`The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security`
   - **Authors**：Yajie Yin（ORCID：0009-0001-6168-2530）
   - **Abstract**：复制 `paper2/submission.md` §3 纯文本版（1712 字符，已程序化验证）
   - **Comments**：复制下面这版（273 字符）
   - **Subject Category**：Primary `cs.CL`（你已有背书）；Secondary 加 `cs.AI`、`cs.CR`（交叉无需背书）
   - **License**：CC-BY 4.0
   - **File**：上传 `paper2/paper.pdf`，格式 **PDF only (no source)**
   - 五个可选字段（Report number / Journal ref / DOI / ACM / MSC）→ **全留空**
3. 预览检查：12 页、表格渲染正常 → **Submit**
4. **点 arXiv 验证邮件确认链接**（不点卡 pending）
5. 等公布（周日至周四 20:00 ET）

## Comments（复制这版）

```
Code and data: https://github.com/1549080929-debug/math_agent
Keywords: agent security; prompt injection; verification; completeness; LLM agents
Writing and implementation assisted by an AI language model; all experiments, data, and research decisions are the author's own.
```

## 与第一篇的关系（供 Comments 或正文引用）

- 本文引用第一篇（arXiv:2608.19009）的 VAL 框架、可复现性（κ≈0.8）、锚语义与完备性盲区；
- 两篇构成"框架 + 应用实证"连续研究线；第一篇 v2 已公布（2608.19009v2）。

## 投稿后

- 状态：Submitted → 验证邮件 → moderation → 公布（cs.CL 主类目下与第一篇并列）
- 公布后更新 README/STATUS.md 链接
- 若想投 2027 会议（ARR→EMNLP 周期），arXiv 记录是最佳起点
