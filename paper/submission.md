# arXiv 提交包（copy-paste 用）

> 生成：2026-08-18 · 用途：arxiv.org 提交表单直接复制粘贴。
> 注意：arXiv 表单不接受 Markdown（`**`、反引号、`*斜体*` 不渲染）——以下摘要已清洗为纯文本。

---

## 1. Title（标题）

```
Grading the Graders: Verification Autonomy Levels (L0–L5) for LLM Reasoning
```

## 2. Authors（作者）

```
Yajie Yin
```

## 3. Abstract（摘要，纯文本版）

```
Large language models (LLMs) are increasingly paired with "verifiers"—step checkers, self-consistency filters, tool-based fact checkers, and formal proof assistants—that claim to detect the model's errors. Yet the verification literature uses the word "level" to mean at least five different things: verification granularity, concept abstraction, risk tier, system-stack layer, and the epistemic source of the ground truth. We propose Verification Autonomy Levels (VAL), a meta-standard that classifies any verification scheme along a single axis: where does the verification spec come from, and what does the verdict guarantee? VAL ranges from L0 (LLM self-declaration; no deterministic anchor) through L2 (objective ground truth; correctness only) to L3/L4 (decidable systems with single-property or domain-level completeness), with L5 shown to be undecidable via Rice's theorem. Central to VAL is the completeness blind spot: substitution- and sampling-based verifiers can confirm that proposed candidates hold, but cannot prove that no candidate was missed. We document this gap empirically across three domains—symbolic mathematics, behavior monitoring, and medical diagnosis—and in the strongest existing formal-verification baseline, whose own authors note the verifier "focuses on the correctness of each step." We further show that the levels of granularity, concept hierarchy, risk, and system stack are orthogonal to VAL, resolving a systematic conflation across 17 surveyed papers. We release a runnable classifier (val_standard.py) and the full literature assessment as supplementary material.
```

## 4. Comments（备注，arXiv 表单字段）

```
Code and data: https://github.com/1549080929-debug/math_agent
Keywords: LLM verification; verification autonomy; completeness; ground truth; trustworthy AI
```

## 5. Subject Categories（学科分类）

```
Primary:  cs.AI
Secondary: cs.CL
Optional:  cs.LG
```

## 6. License（许可）

```
CC-BY 4.0（arXiv 推荐）
```

## 7. 提交时表单字段对照

| arXiv 表单字段 | 填什么 |
|---|---|
| Title | 第 1 节 |
| Authors | 第 2 节（可再加 ORCID：0009-0001-6168-2530） |
| Abstract | 第 3 节（纯文本） |
| Comments | 第 4 节 |
| Subject Category | 第 5 节 |
| License | CC-BY 4.0 |
| 上传文件 | preprint.md 渲染的 PDF（或用 LaTeX 排版版）+ Figure 1 矢量图（可选） |

## 8. 提交前确认（终审清单）

- [x] 标题定稿
- [x] 作者 + 邮箱 + ORCID（无机构，arXiv 允许）
- [x] 摘要（纯文本已清洗，无 Markdown）
- [x] 17 篇相关工作 + 4 篇 arXiv ID 全部核实
- [x] 诚实负结果保留（16/15/13 vs 20/20）
- [x] 伦理边界声明（医疗章：合成病例、非诊断工具）
- [ ] Figure 1 矢量版（mermaid/ASCII 可先用，不影响提交）
- [ ] 实际提交操作（需要 arXiv 账号 + endorsement，须用户本人执行）
