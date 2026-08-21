# arXiv 提交包（第二篇：The Anchor Decides）

> 生成：2026-08-20。主稿：`paper2/paper.md`（9 页，`py paper2/build_paper2.py` 重建 PDF）。
> 类目建议：主 cs.CL（已有背书）+ 交叉 cs.AI、cs.CR（交叉无需背书；若想主 cs.CR 需另申请背书）。

## 1. Title（ASCII 安全）

```
The Anchor Decides: Verification Autonomy Levels Predict the Success of LLM-Agent Security Defenses
```

## 2. Authors

```
Yajie Yin
```

## 3. Abstract（纯文本，需 ≤1920 字符且 ASCII 安全——见 `abstract_v2.txt` 同款处理）

```
Large language model (LLM) agents are increasingly paired with security defenses that claim to make them safe, yet the field lacks a pre-purchase question: what does a given defense actually guarantee, and where does that guarantee come from? We apply Verification Autonomy Levels (VAL, arXiv:2608.19009), a taxonomy that grades verification and authorization schemes by the source of their spec (L0: LLM self-declaration; L1: deterministic rules; L2: objective ground truth, correctness only; L3/L4: decidable systems with single-property or domain-level completeness; L5: impossible), to 22 agent-security defenses. The classification is a falsifiable predictor: a defense fails the way its anchor fails. We validate this on published data (10/10 prediction hits) and run the first controlled deployment-value comparison: same budget, two stacks, a VAL-selected stack (intent-anchored confirmation gate plus schema sandbox) versus a mainstream intuition stack (prompt hardening plus keyword filter), across 50 scenarios, 12 attack families including third-party AgentDojo payloads, real tool effects, adaptive, white-box and PAIR-style attacks, and three seeds (about 5,400 LLM calls). The VAL stack holds 0.000 attack success with 1.000 benign success in every condition; the intuition stack also reaches 0.000 ASR but destroys all benign actions, and its security is model-behavior luck (compliance 0.235), not structure (the VAL stack tolerates 2.4x more model compromise, 0.567 compliance, and still blocks everything). The same zero, two different guarantees. We further identify where L3 anchors exist in agent security: confinement and information-flow properties, not semantic safety, which caps at L2.
```

> 注意：上方为投稿版（含简写）；`paper.md` 正文用完整版。若超 1920 字符，删"including third-party AgentDojo payloads"等从句。

## 4. Comments（备注，≤400 字符）

```
Code and data: https://github.com/1549080929-debug/math_agent
Keywords: agent security; prompt injection; verification; completeness; LLM agents
Writing and implementation assisted by an AI language model; all experiments, data, and research decisions are the author's own.
```

## 5. Subject Categories

```
Primary:   cs.CL（已有背书）
Secondary: cs.AI, cs.CR（交叉无需背书）
```

## 6. License

```
CC-BY 4.0
```

## 7. 提交表单对照

| arXiv 表单字段 | 填什么 |
|---|---|
| Title | 第 1 节 |
| Authors | 第 2 节（ORCID：0009-0001-6168-2530） |
| Abstract | 第 3 节纯文本版（先程序化验证长度与字符集） |
| Comments | 第 4 节 |
| Subject Category | 第 5 节 |
| License | CC-BY 4.0 |
| 上传文件 | paper2/paper.pdf（PDF only） |
| Report number / Journal ref / DOI / ACM / MSC | 全留空 |

## 8. 与第一篇的关系

- 本文是 [Grading the Graders](https://arxiv.org/abs/2608.19009) 的**应用实证篇**：第一篇给框架，第二篇把框架用到 Agent 安全并测部署价值；
- 引用 [1] 的等级体系、可复现性（κ≈0.8）、锚语义（docs/13）与完备性盲区；
- 两篇可互为引用，构成"框架 + 应用"的连续研究线。
