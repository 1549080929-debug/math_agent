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

Large language models (LLMs) produce fluent, confident, and frequently wrong reasoning. The dominant mitigation is *verification*: attach a second mechanism that checks the model's claims. The 2023–2025 literature is a torrent of verification proposals—trained step verifiers [3], self-checking schemas [5], tool-augmented fact checkers [17], graph-structured verification [2], and formal proof assistants [4]—each claiming to catch the errors the model cannot self-report. This proliferation raises a question that the literature has not explicitly asked: **what can a given verification scheme actually guarantee, and where does that guarantee come from?**

Answering this question is harder than it appears, because the field uses the word *level* to mean at least five different things:

1. **Granularity**—how finely the output is decomposed for checking: claim → sentence → document [7]; atomic step → paragraph [2].
2. **Concept abstraction**—the mathematical sophistication at which verification operates: foundational elements → high-level concepts [8].
3. **Risk/disposition**—what the verdict triggers: safe/unsafe/conditional tiers [10]; output-determinism tiers [12].
4. **System stack**—which component is audited: model → workflow → system [13]; data → base → execute → service [14].
5. **Epistemic anchoring**—the source of the ground truth a verdict rests on, and the strength of the guarantee it delivers.

Axes 1–4 answer *what* to check, *how finely*, *at which layer*, and *what to do with the result*. None answers the question that determines whether a verifier can ever be trusted: **on what ground truth does the verdict rest, and does it guarantee correctness, completeness, or neither?**

We argue that the fifth axis is the one that matters for trust, that it has a natural six-level structure, and that the literature's conflation of the five axes has obscured it. Three observations motivate the framework.

*First, the anchor is what fails.* In our three-domain study (Sec. 5), every verification failure we catalogued was traceable to the anchor, not to the judge: a well-calibrated verifier (42/42 unit cases) was fed wrong subproblems by the LLM it was checking (decomposition contamination), never saw the final answer it should have checked (combination tampering), or was asked to verify a condition declared by the very model under test (trust recursion). A perfectly calibrated instrument pointed at the wrong object is not a bug; it is a specification problem.

*Second, correctness is not completeness.* The most common verifiers—substitution, sampling, statistical thresholds—can confirm that *proposed* candidates hold, but cannot prove that *no* candidate was missed. We call this the **completeness blind spot** and document it empirically in symbolic mathematics (a missed root that substitution cannot see), in behavior monitoring (a covert-execution attack that leaves no trace in the output layer), and in medical diagnosis (confident conclusions from insufficient evidence). The blind spot is not a tuning failure; it is a property of the verification paradigm (Sec. 4).

*Third, the strongest existing verification concedes the same point.* The most rigorous scheme in our survey—Lean 4 step-level formal verification [4]—states that its formal verifier "focuses on the correctness of each step": the kernel checks proofs of LLM-generated statements, but the statements themselves, and the case coverage they encode, remain LLM declarations. The blind spot does not disappear at the top of the ladder; it is pushed to the statement layer.

**Contributions.** We make four:

1. **Verification Autonomy Levels (VAL)**, a six-level epistemic taxonomy (L0–L5) classifying any verification scheme by its anchor source and guarantee, together with a deterministic decision procedure (Sec. 3) and a runnable classifier (`val_standard.py`).
2. **A disambiguation of five confounded "level" axes**, showing that granularity, concept abstraction, risk, and system-stack are orthogonal to the VAL axis, and locating 17 representative papers in the resulting space (Sec. 2).
3. **A formal and empirical treatment of the completeness blind spot**, including a statement of why universal completeness is undecidable (Rice's theorem) and why completeness is always relative to an operational design domain (Sec. 4).
4. **Three cross-domain case studies**—symbolic mathematics, behavior monitoring, medical diagnosis—that exercise the framework end-to-end and report honest negative results (Sec. 5).

**Why this matters.** For a deployer, VAL is a pre-purchase checklist: ask *where the spec comes from* before trusting any verification claim, and know that an L2 verdict is a correctness probe, not a completeness guarantee. For a researcher, VAL separates the five questions hidden inside "hierarchical verification," preventing category errors such as claiming that finer granularity implies stronger grounding. For a reviewer, VAL supplies a vocabulary for interrogating any claim of the form "our system verifies X": *at what level, within what ODD, with what abstention behavior?*

---

## 2. Related Work: Five Axes, One Word

We reviewed 17 representative papers spanning what the literature calls "layered" or "hierarchical" verification, and classified each along five axes. The full assessment—per-paper evidence, confidence levels, and a versioned re-verification trail—is released as supplementary material (`docs/07-文献评述.md`); here we report the axis structure and the anchor-axis classifications used throughout.

### 2.1 Granularity axis: *how fine*

Graph of Verification [2] adapts verification granularity from atomic steps (formal tasks) to whole paragraphs (informal narratives) via a "node block" architecture, trading precision against robustness. Factcheck-GPT [7] annotates factuality at three granularities—claim, sentence, document—with a GPT-4-based annotation scheme and a gold-labeled benchmark. Dr. V [9] decomposes video-hallucination diagnosis into perceptual, temporal, and cognitive levels, grounding the first two in 10k spatial-temporal gold annotations. These are ladders of *decomposition fineness*. They say nothing about the anchor: the same granularity ladder can be implemented with LLM judgment (L0) or with objective ground truth (L2).

### 2.2 Concept axis: *how abstract*

Hierarchical Attention [8] regularizes LLM attention toward a five-level hierarchy of mathematical concepts to improve proof generation in formal theorem proving (miniF2F, ProofNet). Its proofs are checked by a formal kernel—an L4 anchor—but the paper's contribution is a generation-time regularizer, and its "levels" are concept-abstraction levels, orthogonal to the anchor.

### 2.3 Risk/disposition axis: *what to do*

A safety-response framework [10] classifies inputs into four disposition tiers (Safe, Unsafe, Conditionally Safe, Focused Attention) via a supervised fine-tuned classifier, reporting 99.3% recall. LLM Output Drift [12] tiers models by output determinism for risk-adapted deployment in finance, combining consistency measurement with invariant checking and SEC-citation validation. M³-SafetyBench [11] evaluates models across content- and functional-safety dimensions with a 170k-item benchmark. These are ladders of *consequence*—what the verdict should trigger. A "four-tier safety classifier" and a "three-level fact-checking pipeline" are frequently cited together, yet one is a disposition ladder and the other a granularity ladder; neither is an epistemic ladder.

### 2.4 System-stack axis: *which layer*

Standard Benchmarks Fail [13] proposes stress-testing financial LLM agents at model, workflow, and system layers, arguing that standard accuracy benchmarks "provide an illusion of reliability." Prompting Frameworks Survey [14] organizes prompting tooling into data, base, execute, and service layers. These are ladders of *audit scope*. [13] is notable as the one paper in our survey that makes completeness of evaluation coverage an explicit thesis.

### 2.5 Anchor axis: *on what ground truth* (this paper)

Classified by the procedure of Sec. 3.3:

- **L0** — SelfCheck [5]: four-stage regenerate-and-compare, explicitly "without resorting to external resources"; the checker itself scores 66.7% verification accuracy and the authors concede "the checks are themselves imperfect." LM² [6]: a verifier language model, fine-tuned on GPT-4 annotations and coordinated with the decomposer and solver via policy learning.
- **L0/L1 + tools** — VerifiAgent [1]: meta-verification of completeness and consistency performed by the agent itself; tool-based adaptive verification delegates factual and computational checks to a Python interpreter, a search engine, and symbolic computation.
- **L1/L2** — Factcheck-GPT [7]: verdicts from a GPT-4-based annotation scheme, with gold labels in its benchmark. FACTOOL [17]: tools (Google Search, Google Scholar, code interpreters) gather evidence, but the final factuality verdict is LLM reasoning over that evidence. LLM Output Drift [12]: consistency measurement plus invariant checking with SEC-citation validation.
- **L2** — DiVERSE [3]: a DeBERTa-v3 step verifier trained on step labels derived by matching against ground-truth answers. M³-SafetyBench [11]: a gold-labeled evaluation benchmark. Dr. V [9]: hallucination diagnosis grounded in gold spatial-temporal annotations.
- **L3/L4** — Hierarchical Attention [8]: proofs checked by a formal kernel. Safe [4]: Lean 4 step verification—the kernel is L4, but the theorem statements are LLM-generated, i.e., L0 at the statement layer.

| Axis | Question it answers | Representative papers |
|---|---|---|
| **Anchor (VAL)** | What ground truth does the verdict rest on, with what guarantee? | SelfCheck L0; LM² L0; VerifiAgent L0/L1+tools; DiVERSE L2; FACTOOL L1/L2; Safe L4+L0 |
| Granularity | How finely is the output decomposed for checking? | GoV, Factcheck-GPT, Dr. V |
| Concept | At what abstraction level does verification operate? | Hierarchical Attention |
| Risk/Disposition | What response does the verdict trigger? | SafetyResponse, OutputDrift, M³-SafetyBench |
| System stack | Which component of the system is audited? | BenchmarksFail, PromptingSurvey |

**Observation.** Across all 17 papers, none formalizes the anchor as a ladder, none treats the completeness of a verification scheme itself as an object of study, and the single most explicit acknowledgment of the gap comes from the strongest formal baseline [4]. The conflation is not harmless: it lets "layered verification" papers inherit each other's credibility across axes that do not entail one another. The rest of this paper develops the anchor axis.

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

Each level is defined by two properties: the **anchor source** (who or what supplies the ground truth the verdict rests on) and the **guarantee** (what a PASS commits to). Three consequences follow.

First, *the anchor, not the judge, determines the level.* A perfectly calibrated verifier at L2 is still L2: substitution checking that a candidate satisfies an equation proves the candidate holds; it says nothing about candidates not proposed. Improving the *implementation* of an L2 check (denser sampling, a better threshold) moves the system horizontally within L2; only changing the anchor source moves it vertically.

Second, *the guarantee degrades downward but not upward.* A judge built for L3 (e.g., a symbolic solver) can be *used* at L2 (substitution only)—we call this a *usage-degraded* anchor, and the classifier flags it as upgradeable. A judge built for L2 cannot be promoted to L3 by more data: no amount of sampling closes a completeness gap (Sec. 4). This asymmetry is why "more data" is not a level-raising operation.

Third, *every level has a characteristic abstention behavior.* The most honest judges abstain. L0 systems deny error—they "confidently err." L1/L2 systems are silent about what they did not check. L3/L4 systems return a decidable UNSURE-equivalent when a property falls outside their ODD (Safe's "failed formalization" state is exactly this [4]). L5 does not exist. In our experience, a verifier's abstention behavior is a faster diagnostic of its level than any benchmark score.

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

Any verification scheme is classified by answering three questions in order:

- **Q1 (spec source).** Who declares the verification condition—the thing the verdict is about? The answer is one of: (a) the LLM under test itself ("I checked it," "this is verified"); (b) a deterministic rule derived from the problem or code text (regex, parser, schema); (c) an objective source independent of the problem (gold answer, measured value, external oracle); (d) a property encoded in a decidable system (a symbolic solver, a type system, a decision rule with validated thresholds).
- **Q2 (guarantee).** What does a PASS commit to? *Correctness*—"every proposed candidate satisfies the condition"—or *completeness*—"no candidate was missed." The distinction is the entire substance of Sec. 4; most deployed verifiers offer the former while being read as the latter.
- **Q3 (scope).** If the guarantee is completeness, over what domain does it hold: a single property (this equation's solution set), a whole class (all programs' memory safety), or claimed universality?

### 3.3 Decision procedure

The classification is deterministic: given the answers to Q1–Q3, the level is the first rule that fires.

```
1. completeness + universal scope        → L5   (rejected: undecidable, Rice)
2. completeness + domain scope           → L4
3. completeness + single-property scope  → L3
4. correctness + decidable or objective anchor → L2
     (decidable anchor used only for correctness → flag "usage-degraded, upgradeable")
5. correctness + problem-derived rule    → L1
6. otherwise (LLM-declared / no anchor)  → L0
```

The procedure is implemented in `val_standard.py` (10 self-tests) and documented in `docs/06-判级标准.md`. Its determinism is deliberate: it is a *standard*, so two raters applying it to the same scheme must obtain the same level; the only legitimate disagreements concern the Q1/Q2 answers, not the mapping.

### 3.4 Operational Design Domain (ODD)

Borrowing from autonomous-driving regulation, an L3/L4 guarantee holds only within an **ODD**—here, the *decidable domain* in which the property can be encoded and the verdict computed. Examples: solution-set equivalence via `solveset` has an ODD of "single-variable algebraic equations and inequalities that the solver can solve in closed form"; an Alvarado score has an ODD of "suspected appendicitis with all eight objective inputs present"; a Rust borrow checker has an ODD of "memory-safety properties expressible in the ownership/borrowing/lifetime type language."

Two corollaries. First, **completeness is never absolute; it is relative to an ODD.** A verifier that is complete inside its ODD is, by construction, silent about anything outside it—the completeness claim is only as strong as the ODD is honestly specified. Second, **raising a level means enlarging the ODD, not intensifying sampling.** The L2→L3 move for "find all solutions" is achieved by re-encoding the task as solution-set equality, making the property decidable; no sampling density achieves this. The L3→L4 move is achieved by covering a whole class of properties under one decidable system.

### 3.5 What VAL is not

Three non-claims, to preempt misreading:

1. **VAL is not a reliability measure.** A level states the epistemic status of an anchor; it does not state the probability that a verdict is correct. An L2 verifier can be more *accurate* than an L3 verifier on in-ODD cases (our own 42/42 unit tests span L2 and L3); level and reliability are orthogonal.
2. **VAL is not a utility claim.** We do not argue that higher is always better, nor that L3/L4 should be pursued everywhere. Sec. 6 governs *when* climbing is worth its cost; for low-stakes tasks an honest L1/L2 check may be the correct engineering choice.
3. **VAL does not certify the anchor.** An L3 anchor guarantees that, *given the encoded property*, the verdict is decidable and complete. It does not guarantee that the property is the right one—that question is itself an anchor question, one level up (Sec. 6). This is the framework's own form of the regress it describes.

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
