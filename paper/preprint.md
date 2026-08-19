# Grading the Graders: Verification Autonomy Levels (L0–L5) for LLM Reasoning

<!-- 骨架稿 v0.1 (2026-08-18)。[TODO] 为待补内容；正文为草稿级英文，可改写。 -->

## Abstract

Large language models (LLMs) are increasingly paired with "verifiers"—step checkers, self-consistency filters, tool-based fact checkers, and formal proof assistants—that claim to detect the model's errors. Yet the verification literature uses the word *level* to mean at least five different things: verification granularity, concept abstraction, risk tier, system-stack layer, and the epistemic source of the ground truth. We propose **Verification Autonomy Levels (VAL)**, a meta-standard that classifies any verification scheme along a single axis: *where does the verification spec come from, and what does the verdict guarantee?* VAL ranges from L0 (LLM self-declaration; no deterministic anchor) through L2 (objective ground truth; correctness only) to L3/L4 (decidable systems with single-property or domain-level completeness), with L5 shown to be undecidable via Rice's theorem. Central to VAL is the **completeness blind spot**: substitution- and sampling-based verifiers can confirm that proposed candidates hold, but cannot prove that no candidate was missed. We document this gap empirically across three domains—symbolic mathematics, behavior monitoring, and medical diagnosis—and in the strongest existing formal-verification baseline, whose own authors note the verifier "focuses on the correctness of each step." We further show that the levels of granularity, concept hierarchy, risk, and system stack are orthogonal to VAL, resolving a systematic conflation across 17 surveyed papers. We release a runnable classifier (`val_standard.py`) and the full literature assessment as supplementary material.

**Keywords**: LLM verification, verification autonomy, completeness, ground truth, trustworthy AI

<!-- ✅ 标题已定稿（2026-08-18）：A. Grading the Graders: Verification Autonomy Levels (L0–L5) for LLM Reasoning
备选（未选）：
B. The Judge of Judges: A Verification Autonomy Framework for LLM Reasoning
C. Beyond Self-Checking: Verification Autonomy Levels and the Completeness Blind Spot
-->

---

## 1. Introduction

LLMs produce fluent, confident, and frequently wrong reasoning. The dominant mitigation is *verification*: attach a second mechanism that checks the model's claims. In 2025 alone, proposals range from trained step verifiers [DiVERSE], self-checking schemas [SelfCheck], tool-augmented fact checkers [FACTOOL], graph-structured verification [GoV], and formal proof assistants [Safe]. This proliferation raises a question that the literature has not explicitly asked: **what can a given verification scheme actually guarantee, and where does that guarantee come from?**

Answering this question is harder than it appears, because the word "level" is used inconsistently across the field:

- *Granularity* levels (claim → sentence → document [Factcheck-GPT]; atomic step → paragraph [GoV]);
- *Concept* levels (foundational element → high-level concept [Hierarchical Attention]);
- *Risk* tiers (Safe / Unsafe / Conditionally Safe [SafetyResponse]; output-determinism tiers [OutputDrift]);
- *System-stack* layers (model → workflow → system [BenchmarksFail]; data → base → execute → service [PromptingSurvey]);
- *Epistemic* levels—the source and strength of the ground truth a verifier anchors to.

The first four axes answer *what* to check, *how finely*, *at which layer*, and *what to do with the result*. None answers the question that determines whether a verifier can ever be trusted: **on what ground truth does the verdict rest, and does it guarantee correctness, completeness, or neither?**

We contribute:

1. **VAL**, a six-level epistemic taxonomy (L0–L5) that classifies any verification scheme by its anchor source and guarantee (Sec. 3).
2. **A disambiguation of five confounded "level" axes**, showing that granularity, concept, risk, and system-stack are orthogonal to VAL (Sec. 4)—resolving the conflation observed across 17 surveyed papers.
3. **A formal and empirical treatment of the completeness blind spot**: substitution- and sampling-based verification cannot prove that no candidate was missed; we show this in symbolic mathematics, behavior monitoring, and medical diagnosis, and cite the strongest formal-verification baseline's own admission of the gap (Sec. 6).
4. **A runnable classifier** (`val_standard.py`) and a fully versioned literature assessment (docs/07), both released as supplementary material.

<!-- [TODO] 加一段"为什么这重要"：对部署者的价值（选验证器时先问锚定层级）、对研究者的价值（区分正交轴）、对审阅者的价值（判定声称） -->

---

## 2. Related Work: Five Axes, One Word

We reviewed 17 representative papers spanning "layered/hierarchical verification" and classified each along the five axes. Full details (with per-paper evidence and versioned re-verification) are in `docs/07-文献评述.md`. Here we summarize the axis structure; the anchor-axis classifications are used throughout.

| Axis | Question it answers | Example papers |
|---|---|---|
| **Anchor (VAL)** | What ground truth does the verdict rest on? | SelfCheck L0; LM² L0; VerifiAgent L0/L1+tools; DiVERSE L2; FACTOOL L1/L2; Safe L4+L0 |
| Granularity | How finely is the output decomposed for checking? | GoV, Factcheck-GPT, Dr.V |
| Concept | What abstraction level does the verifier operate at? | Hierarchical Attention |
| Risk/Disposition | What response does the verdict trigger? | SafetyResponse, OutputDrift, M³-SafetyBench |
| System stack | Which component of the system is audited? | BenchmarksFail, PromptingSurvey |

The anchor axis is the only one that determines the *epistemic* strength of a verdict, and it is the one axis the literature never formalizes as a ladder. The remaining sections develop it.

---

## 3. The VAL Framework

### 3.1 Levels

| Level | Anchor source | Guarantee | Completeness | Driving analogy |
|---|---|---|---|---|
| **L0** | LLM self-declaration | none | none | full manual (the driver "confidently errs") |
| **L1** | deterministic rules derived from the problem text/code | deterministic matching | no | lane keeping (single-function assist) |
| **L2** | objective ground truth / oracle / gold labels | correctness | no | partial automation (human must take over) |
| **L3** | definitional/provable (property encoded in a decidable system) | single-property **completeness** | yes (within ODD) | conditional automation (system owns liability in ODD) |
| **L4** | domain-level proof systems | domain-wide completeness | yes (within domain) | high automation (no takeover in ODD) |
| **L5** | universal completeness | any property | **undecidable** (Rice) | full automation—does not exist |

<!-- Figure 1 (mermaid 版) -->

```mermaid
pyramid
  title Verification Autonomy Levels (VAL)
  "L5 · universal completeness — undecidable (Rice)" : 1
  "L4 · domain-level proof systems (type systems, proof kernels)" : 2
  "L3 · decidable system, single-property complete (solveset, decision rules)" : 3
  "L2 · objective ground truth / oracle — correctness only (substitution, sampling)" : 4
  "L1 · deterministic rules derived from problem text/code" : 5
  "L0 · LLM self-declaration ("I checked it")" : 6
```

<!-- Figure 1 (ASCII 版，供任意渲染环境) -->

```
        ▲  VAL axis (anchor source & guarantee) — THIS PAPER
        │
   L5 ──┼── universal completeness ── undecidable (Rice's theorem)
   L4 ──┼── domain proof systems (type systems, proof kernels)
   L3 ──┼── decidable system, single-property COMPLETE (solveset, decision rules)
   L2 ──┼── objective truth / oracle ── correctness ONLY (substitution, sampling)
   L1 ──┼── deterministic rules from problem text/code
   L0 ──┼── LLM self-declaration ("I checked it")
        │
        └──────┬──────────────┬──────────────┬──────────────────┬──────────────▶
               │              │              │                  │
         granularity     concept       risk/disposition    system stack
         (how fine:      (abstraction  (what response:     (which layer:
          claim→doc)      level)        safe→focused)       model→system)
```

**Figure 1.** The VAL ladder (vertical) and four orthogonal axes (horizontal) that the literature
conflates with it. Granularity, concept, risk, and system-stack answer *what / how fine / what
response / which layer*; VAL answers *on what ground truth, with what guarantee*.
<!-- [TODO] 正式版：用矢量图工具重绘，arXiv 需 PDF/EPS/PNG -->

### 3.2 The three decisive questions

Any verification scheme is classified by answering:

- **Q1 (spec source)** — who declares the verification condition? *LLM / problem-derived rule / objective truth / decidable system.*
- **Q2 (guarantee)** — correctness (given candidates hold) or completeness (no candidate missed)?
- **Q3 (scope)** — if complete: single property, whole domain, or claimed universal?

### 3.3 Decision procedure

1. completeness + universal scope → **L5** (rejected; Rice's theorem)
2. completeness + domain scope → **L4**
3. completeness + single property → **L3**
4. correctness + decidable/objective anchor → **L2** (decidable anchors used only for correctness are *usage-degraded* and upgradeable)
5. correctness + problem-derived rule → **L1**
6. otherwise (LLM self-declared / no deterministic anchor) → **L0**

### 3.4 Operational Design Domain (ODD)

Borrowing from autonomous-driving regulation, L3/L4 guarantees hold only within an **ODD**—here, the *decidable domain* in which the property can be encoded. `solveset`-based solution-set equivalence has an ODD of "single-variable algebraic equations/inequalities that SymPy can solve in closed form"; Alvarado scoring has an ODD of "suspected appendicitis with the eight objective inputs"; a type system has an ODD of "properties expressible in the type language." **Completeness is never absolute; it is relative to an ODD.** Raising a system's level means enlarging its ODD, not "trying harder" at sampling.

---

## 4. The Completeness Blind Spot

The central theoretical claim of this paper:

> **Substitution- and sampling-based verification (L2) can prove that proposed candidates hold; it cannot prove that no candidate was missed. Completeness is achievable only by re-encoding the property into a decidable system (L3/L4)—or not at all.**

Three kinds of evidence:

**Empirical (symbolic mathematics).** In our math agent, substitution verification of the candidate *a = 2* passed for a problem whose true answer is *{0, 2}*; the missed candidate *a = 0* is invisible to substitution by construction. Re-encoding the problem as solution-set equality via `solveset` (an L3 anchor) converts the blindness into a decidable FAIL: claimed `"2"` vs. true `{2, 3}`. Sampling-based final-parameter verification exhibits a *sampling ceiling*: in our 20-problem run, all three false passes stemmed from candidates/voids the sampler did not hit.

**Empirical (behavior monitoring).** A statistical deviation detector (L2, threshold from a baseline distribution) reached 30% FPR at strong-attack TPR 1.0, but could not detect "covert execution" attacks (TPR 0.60) because the property leaves no trace in the output layer—the property cannot be encoded into the anchor at all.

**The strongest baseline's own admission.** The most rigorous verification scheme in our survey—Lean 4 step-level formal verification [Safe]—states: *"our formal verifier focuses on the correctness of each step."* The formal kernel checks proofs of LLM-generated statements; the statements themselves, and the case-split coverage they encode, remain LLM declarations. This is the completeness blind spot pushed to the statement layer, not resolved.

<!-- [TODO] 3.4 的"完备性可判定性"小节：L5 不可判定的严格表述（Rice），及"信任递归必须收敛到可审计原子"的论证 -->

---

## 5. Empirical Case Studies

We exercised the framework across three domains. Full experiment archives are in the repository (`RESULTS.md`, `behavior/REPORT.md`, `medical/REPORT.md`). Summary:

### 5.1 Symbolic mathematics (Chapter 1)

- A deterministic SymPy verifier was calibrated with **42/42** unit cases (L2–L3 depending on verification type; `ANCHOR_LEVELS` in `verifier.py`).
- **Honest negative result**: on a 20-problem test set, the full decompose–verify–combine architecture scored 16/15/13 across three runs, while the raw LLM baseline scored 20/20. Accuracy is a random variable dominated by LLM decomposition; verification did not improve it. We do not claim otherwise.
- The architecture's value is not accuracy but *error reportability*: it turned silent errors into labeled ones (e.g., catching `[-1,1]` → correcting to `[0,1]`), and the `solution_set` (L3) verifier catches missed solutions that substitution cannot.

### 5.2 Behavior monitoring (Chapter 2)

- Five iterative rounds moved a statistical detector from an illusory AUC 0.82 to a deployable window: probe-conditioning cut FPR from 92% to 30%; semantic embeddings recovered weak-attack TPR from 0.50 to 0.75. The residual boundary—covert execution at TPR 0.60—is an L2 ceiling, not a tuning failure.

### 5.3 Medical diagnosis (Chapter 3)

- Raw LLM diagnosis: 10/10 textbook, 8/10 hard cases; the failure mode was "confident conclusion from insufficient evidence" (#103, #104).
- An information-completeness judge (a deterministic post-hoc rule, L2) flagged 3/3 true failures—**including one (#105) missed by human review**—at 0 false positives after calibration. This illustrates the judge's value as *discovery*, not merely re-checking.

<!-- [TODO] 5.4 医疗章接 L3（Alvarado 等决策规则）后作为"抬级成功"案例；若未完成则标注为 future work -->

---

## 6. Discussion

**Trust recursion and its termination.** Every judge needs a judge; ungrounded chains are *trust recursion*. The framework shows where recursion can terminate: at the kernel of a decidable system (L4), at a definitional anchor (L3), or at a conventional primary standard (metrology). L5 is the claim that recursion can be terminated universally—which Rice's theorem rules out.

**Division of labor.** VAL implies a canonical architecture: the LLM translates (decomposes, renders), deterministic code judges (within its ODD), and a human anchors the spec and audits the judge. Each component is best at what the others cannot do: the LLM cannot prove, the judge cannot generalize, the human cannot scale.

**When to climb.** The decision to raise a verifier's level is governed by two factors: the cost of silent errors (high in medical/safety/finance) and the encodability of the property (ODD availability). High cost + encodable ⇒ L3/L4 is mandatory; otherwise L1/L2 is honest and sufficient. The framework therefore functions as a *deployment checklist*, not a competition ladder.

---

## 7. Limitations

1. **Literature assessment is abstract-level for 11 of 17 papers**; 6 anchor-axis papers were verified against full text (`docs/07` V1.3). The classification of the remainder may shift with full-text review, though the axis structure is unaffected.
2. **Case studies use a single model family** (deepseek-chat) and synthetic data (medical cases are fictional; no patient data).
3. **VAL classifies, it does not measure**: a scheme's level states its anchor's epistemic status, not the probability that its verdict is correct. Level and reliability are orthogonal.
4. **ODD boundaries are fuzzy in practice**: whether a property is "encodable" depends on the solver, the type system, or the rule's inputs, and can change with tooling.

---

## 8. Conclusion

The verification literature for LLMs is a tower of levels built on different questions. We have argued that one question—*where does the ground truth come from, and what does the verdict guarantee?*—underlies all claims of verification strength, and we have provided a six-level taxonomy (VAL, L0–L5), a decision procedure, and a runnable classifier. Our empirical case studies and literature review support a single headline claim:

> **Others grade answers. We grade the graders—and the highest grade any grader can earn is a guarantee it can actually deliver: correctness within its domain, completeness within its ODD, and honesty when it must abstain.**

---

## References

1. Han, J., Buntine, W., Shareghi, E. *VerifiAgent: A Unified Verification Agent in Language Model Reasoning.* arXiv:2504.00406, 2025.
2. Fang, J., Zhang, B., Wang, C., et al. *Graph of Verification (GoV): Structured Verification of LLM Reasoning with Directed Acyclic Graphs.* arXiv:2506.12509, 2025.
3. Li, Y., Lin, Z., Zhang, S., et al. *Making Large Language Models Better Reasoners with Step-Aware Verifier (DiVERSE).* ACL 2023.
4. Liu, C., Yuan, Y., Yin, Y., et al. *Safe: Enhancing Mathematical Reasoning in LLMs via Retrospective Step-aware Formal Verification.* ACL 2025.
5. Miao, N., Teh, Y.W., Rainforth, T. *SelfCheck: Using LLMs to Zero-Shot Check Their Own Step-by-Step Reasoning.* ICLR 2024. arXiv:2308.00436.
6. Juneja, G., Dutta, S., Chakraborty, T. *LM²: A Simple Society of Language Models Solves Complex Reasoning.* EMNLP 2024.
7. Wang, Y., Gangi Reddy, R., et al. *Factcheck-GPT: End-to-End Fine-Grained Document-Level Fact-Checking and Correction of LLM Output.* arXiv:2311.09000, 2023.
8. Chen, J., Li, C., Yuan, Y., Yao, A.C. *Hierarchical Attention Generates Better Proofs.* ACL 2025.
9. Luo, M., Wu, S., et al. *Dr. V: A Hierarchical Perception-Temporal-Cognition Framework to Diagnose Video Hallucination.* arXiv:2509.11866, 2025.
10. Li, Q., Xu, J., et al. *A Proprietary Model-Based Safety Response Framework for AI Agents.* arXiv:2511.03138, 2025.
11. Yang, W., Cheng, H., Zhou, B., et al. *M³-SafetyBench: 多领域多场景多维度的大语言模型安全评估体系.* 中国科学：信息科学, 55:2923–2940, 2025.
12. Khatchadourian, R., Franco, R. *LLM Output Drift: Cross-Provider Validation & Mitigation for Financial Workflows.* arXiv:2511.07585, 2025.
13. Chen, Z., Chen, J., et al. *Standard Benchmarks Fail—Auditing LLM Agents in Finance Must Prioritize Risk.* arXiv:2502.15865, 2025.
14. Liu, X., Wang, J., et al. *Prompting Frameworks for Large Language Models: A Survey.* ACM Computing Surveys. arXiv:2311.12785.
15. Liu, Y., Yao, Y., et al. *Trustworthy LLMs: A Survey and Guideline for Evaluating Large Language Models' Alignment.* arXiv:2308.05374, 2023.
16. González, J., Nori, A.V. *Beyond Words: A Mathematical Framework for Interpreting Large Language Models (HEX).* arXiv:2311.03033, 2023.
17. FacTool: *Factuality Detection in Generative AI—A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios.* ICLR 2024. arXiv:2307.13528.

<!-- [TODO] 附录 A：判级程序（引用 docs/06 + val_standard.py 输出）；附录 B：17 篇判级总表（引用 docs/07）；附录 C：三章实验细节 -->
