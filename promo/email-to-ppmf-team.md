# 邮件：致 PPMF 团队（arXiv:2607.29167）

> 收件人：Jinghan Xu 等作者（邮箱需从 arXiv 页面获取：https://arxiv.org/abs/2607.29167）
> 主题行直接用下面的 Subject。
> 发送前检查：把 [your email signature] 换成你的落款；确认对方对等交流意愿后再谈引用。

---

**Subject: On the structural correspondence between PPMF and Verification Autonomy Levels**

Dear Jinghan Xu and colleagues,

I read "Memory Provenance Laundering in LLM Agents: A Non-Amplification Firewall for Persistent Memory" (arXiv:2607.29167) after a research digest matched it to my own work, and it struck me as the cleanest real-world instance I have seen of a structure I study — so I wanted to reach out.

I work on Verification Autonomy Levels (VAL, arXiv:2608.19009), a taxonomy that classifies verification/authorization schemes by a single axis: where the verification spec comes from, and what the verdict guarantees (L0 = LLM self-declaration with no deterministic anchor; L2 = objective ground truth, correctness only; L3/L4 = decidable systems with single-property or domain-level completeness; L5 = impossible in the unrestricted case).

Three structural correspondences stood out:

1. **Your trust ladder** (UNKNOWN < EXTERNAL < TRUSTEDTOOL < USERHISTORY < USER_CONFIRMED < SYSTEM) is, as far as I can tell, exactly an anchoring axis: an ordering of spec sources by authority.

2. **Your "source-authority non-amplification" invariant** is the same asymmetry VAL identifies — a guarantee can degrade downward but cannot be promoted upward by rewriting. Memory provenance laundering is a *forged-anchor attack*: consolidation changes the memory's apparent anchor without changing its real one. In VAL terms this is trust recursion surfacing at the memory layer — the authority claim is written by the very component (LLM consolidation) whose output is being trusted.

3. **Your design principle** ("the LLM may plan; the platform enforces authority"; the gate reads platform-maintained metadata, not generated text) is what VAL argues is the only way to terminate the recursion: anchor the verification spec in ground truth independent of the LLM's declarations.

Under VAL, I would classify the PPMF gate as **L1/L2** — objective platform metadata (L2 inputs) passed through a designer-specified risk policy (L1 rule), correctness-only, with the completeness blind spot visible in your own results (10% forged confirmations -> ASR 0.088: a correctness probe, not a completeness guarantee).

One thing VAL might add to PPMF's framing: the trust ladder orders sources (the Q1 axis) but does not carry guarantee semantics (Q2/Q3). A USER_CONFIRMED label guarantees the user's *intent for a target*, not that the subsequent action will execute correctly — those are different anchors, and making the distinction explicit clarifies what the gate can and cannot certify.

I would be glad to share our full analysis (maintained openly, with a runnable classifier) and discuss — no obligation. I found the correspondence genuinely interesting and thought your team might too.

Best regards,
Yajie Yin
https://arxiv.org/abs/2608.19009
