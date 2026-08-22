"""最终压缩：§2/§3/§5 精简 + §6.5 ND 段移附录 + §9/§7 精简。目标正文 8 页。"""
import re

p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()
appendix_extra = []

# 1. §2.2 压缩
old = '''The defense literature is large. Text-level defenses (prompt hardening [8], keyword/content filters, Llama Guard [9]) operate on the current context; tool-level defenses (allowlists [10], permission systems [11], information-flow control [12], sandboxes) gate execution; memory-level defenses (A-MemGuard [14], PPMF [2]) protect persistent state; benchmarks (AgentDojo [4]) measure attack success and utility trade-offs. Recent work has begun to move beyond single-defense evaluation: Injection-Execution Dissociation [5] shows that injection success and tool-execution success are separable safety properties (memory storage rates >97.5% while downstream execution ranges 0–95%, uncorrelated); the Source-of-Authority SLR [6] classifies LLM test oracles by where their authority comes from and finds over half reach verdicts with no specification at all; When Does Verification Pay Off [7] shows that same-family verification yields near-zero gain while cross-family verification remains valuable. Our contribution is different in kind: we do not add another defense, we provide a *pre-purchase axis*—the anchor—that organizes the entire landscape and predicts each defense's failure modes, and we measure whether choosing by this axis beats choosing by intuition.'''
new = '''The defense literature spans text-level (prompt hardening [8], filters, Llama Guard [9]), tool-level (allowlists, permission systems, IFC [12], sandboxes), and memory-level (A-MemGuard [14], PPMF [2]) defenses, plus benchmarks like AgentDojo [4]. Recent work separates injection success from execution success [5], classifies test oracles by authority source (over half with no specification [6]), and shows same-family verification yields near-zero gain [7]. Our contribution is different in kind: not another defense, but a *pre-purchase axis*—the anchor—that organizes the landscape and predicts each defense's failure modes, measured against choosing by intuition.'''
assert old in s, '2.2 anchor'
s = s.replace(old, new)

# 2. §3.1 Classification protocol 压缩
old = '''We classify defenses with the frozen VAL protocol (v2.3, [1]), extended for security: R1 benchmarks are N/A (not runtime verifiers); R2 mixed systems are split per component with the weakest anchor on the verdict path reported; R3 evidence anchors do not equal verdict anchors (retrieved documents are L2 evidence; an LLM alignment verdict over them is L0); R4 silver anchors (deterministic recomputation without gold) are L1; R10 designer-authored unvalidated rules are L1; R12b theorem-backed exhaustive procedures (confinement, taint tracking) are decidable (L3); R15 LLM-generated verification expectations place the weakest anchor at L0. Each defense is rated on Q1/Q2/Q3 from a mechanism-only evidence pack by blind raters; classifications reported here are the committed (weakest-anchor) levels. For the security subset (22 agent-security items), two independent blind raters agree exactly on 20/22 (90.9%); the two disagreements are known boundary cases (an LLM-alignment verdict classified under rule R3, and a single-property vs domain completeness scope).'''
new = '''We classify defenses with the frozen VAL protocol (v2.3, [1]) extended for security: R2 mixed systems split per component (weakest anchor on the verdict path); R3 evidence anchors do not equal verdict anchors; R10 designer rules are L1; R12b theorem-backed exhaustive procedures (confinement, taint tracking) are L3; R15 LLM-generated expectations are L0. Each defense is rated on Q1/Q2/Q3 from a mechanism-only evidence pack by blind raters. For the security subset (22 items), two independent raters agree exactly on 20/22 (90.9%); the two disagreements are known boundary cases.'''
assert old in s, '3.1 anchor'
s = s.replace(old, new)

# 3. §3.1 On the validity 压缩
old = '''**On the validity of the taxonomy.** A taxonomy cannot be validated by its own consistency: agreement among raters shows the categories are *usable*, not that they are *right*. We offer three independent lines of evidence instead. First, *out-of-sample prediction*: the level-to-failure-mode cards (Section 3.2) were frozen before outcome data and hit 10/10 on published results, with two mechanism-driven corrections—retrospective storytelling cannot produce that pattern. Second, *cross-benchmark convergence*: the same anchor logic predicts our own testbed results (Section 6), AgentDojo's official numbers (Section 6.5), JADE's MCP instances (Section 6.5), and LITMUS's OS-level behavior (Section 7)—four independent sources with no shared implementation. Third, *falsifiability*: each card names the specific attack predicted to break its defense, so a single well-chosen counterexample refutes the mapping. This is an operational defense: we claim VAL is a productive organizing principle, and we make it easy to disprove—not that it is the unique correct ontology of agent security.'''
new = '''**On the validity of the taxonomy.** Agreement among raters shows the categories are *usable*, not *right*. We offer three independent lines instead: *out-of-sample prediction* (cards frozen before outcome data, 10/10 hits with two mechanism-driven corrections—retrospective storytelling cannot produce that pattern); *cross-benchmark convergence* (the same anchor logic predicts our testbed, AgentDojo, JADE, and LITMUS results—four sources with no shared implementation); and *falsifiability* (each card names the attack predicted to break its defense). We claim VAL is a productive organizing principle, not the unique correct ontology.'''
assert old in s, 'validity anchor'
s = s.replace(old, new)

# 4. §3.2 Prediction protocol 压缩
old = '''Following the reverse-validation discipline of [1], we freeze prediction cards before consulting outcome data: for each defense, level → predicted behavior pattern (ASR regime, bypass mechanism, benign-cost mode) + the specific attack predicted to break it. Cards are signed and dated, then validated against published data (PPMF's own numbers; abstract-level evidence for other systems, flagged as such). The protocol also generalizes out of sample: before running the third-party JADE MCP instances (Section 6.5), we froze five predictions (e.g., N's keyword filter will leak the post_tweet variant, whose action word is absent from the filter's vocabulary; V's sandbox will block every variant by whitelist enumeration regardless of how much the model is driven). All five held on the real MCP harness, including the boundary prediction—the intuition stack leaked exactly the post_tweet case.'''
new = '''Following [1], we freeze prediction cards before outcome data: for each defense, level → predicted behavior pattern + the specific attack predicted to break it, validated against published data (PPMF's numbers; abstract-level evidence flagged as such). The protocol also generalizes out of sample: before running JADE's MCP instances (Section 6.5) we froze five predictions (e.g., N's keyword filter will leak the post_tweet variant—its action word absent from the filter's vocabulary; V's sandbox will block every variant by whitelist enumeration). All five held, including the boundary prediction.'''
assert old in s, '3.2 anchor'
s = s.replace(old, new)

# 5. §5 PPMF family 段压缩
old = '''**PPMF family (6 defenses):** all six predictions hit on PPMF's own published numbers [2]: content filters (L1) leave 0.200–0.933 ASR and collapse under rewriting; Self-Ask provenance (L0) reaches 0.984 ASR; the gate-only ablation (L1 without L2 inputs) blocks attacks but kills all benign actions; the full PPMF (L1/L2: platform metadata through a designer policy) achieves 0.000 ASR on evaluated attacks with benign preserved, and 0.088 ASR under 10% forged confirmations—the completeness blind spot made quantitative.'''
new = '''**PPMF family (6 defenses):** all six predictions hit on PPMF's published numbers [2]: content filters collapse under rewriting; Self-Ask provenance (L0) reaches 0.984 ASR; the gate-only ablation kills benign actions; full PPMF (L1/L2) achieves 0.000 ASR with benign preserved, and 0.088 under 10% forged confirmations—the completeness blind spot quantified.'''
assert old in s, 'PPMF family anchor'
s = s.replace(old, new)

# 6. §6.5 ND 差异段 -> 附录
old_nd = '''**On the varying ND baseline across testbeds.** The undefended ASR differs sharply across our three settings—0.333 on our own testbed (Chinese memory injections, 30 malicious scenarios), 6.2% on AgentDojo (English TODO injections, 144 pairs), 87.5% on JADE's MCP instances (English tool-description poisoning, 16 cases). This is expected and informative rather than a contradiction: ND ASR measures the *attack surface* (injection strength, carrier, environment semantics), not a fixed property of the model. What is stable across all three is the *contrast*: the intuition stack's zero moves with the setting (0.000 → 0.035 → 0.062 as attacks get harder), while V's structural zero does not (0.000 everywhere).'''
if old_nd in s:
    s = s.replace(old_nd, '')
    appendix_extra.append('### A.3 Varying ND baseline across testbeds\n\n' + old_nd.strip())
    print('[ok] ND 段移附录')

# 7. §9 Conclusion 压缩
old = '''The agent-security field has a deployment problem: too many defenses, no pre-purchase axis. We showed that VAL provides one. Across the 22 defenses, attack families, and testbeds we studied, the anchor of a defense predicts how it fails—text rules fail to rewriting, model self-assessment fails to compliance, objective anchors fail outside their ODD, and structural anchors (confinement, information flow, data-control separation) hold by construction within it. In our controlled same-budget comparison, choosing by this axis beat choosing by intuition: identical security numbers, opposite guarantees, and a 100-point utility gap. We also located the L3 frontier in agent security: **confinement, not semantics**—the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should. Two caveats bound these claims: the taxonomy's categories are ours (validated by blind-rater agreement and out-of-sample predictions, not by an external ground truth), and the deployment comparison pits structural defenses against the most common behavioral defenses, not against every defense in the landscape. We offer VAL as a falsifiable framework and a research agenda—not as a settled ontology.'''
new = '''The agent-security field has too many defenses and no pre-purchase axis; we showed that VAL provides one. Across the 22 defenses and testbeds we studied, the anchor predicts how a defense fails—text rules to rewriting, model self-assessment to compliance, objective anchors outside their ODD, structural anchors by construction within it. Choosing by this axis beat choosing by intuition on the same budget: identical security numbers, opposite guarantees, a 100-point utility gap. We located the L3 frontier in agent security: **confinement, not semantics**—the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should. Caveats: the taxonomy's categories are ours (validated by blind-rater agreement and out-of-sample predictions), and the comparison pits structural against the most common behavioral defenses, not against every defense. We offer VAL as a falsifiable framework and a research agenda, not a settled ontology.'''
assert old in s, 'conclusion anchor'
s = s.replace(old, new)

# 附录追加（ND 段）
if appendix_extra:
    if '## Appendix' in s:
        # 在附录末尾追加（References 前）
        ai = s.find('## Appendix')
        # 找附录末尾 = 下一个 ## 或文件尾
        nxt = s.find('\n## ', ai + 10)
        if nxt < 0:
            nxt = len(s)
        insert = '\n\n' + '\n\n'.join(appendix_extra)
        s = s[:nxt] + insert + s[nxt:]
    else:
        s = s.rstrip() + '\n\n## Appendix\n\n' + '\n\n'.join(appendix_extra) + '\n'

open(p, 'w', encoding='utf-8').write(s)
print('压缩完成，字数:', len(s.split()))
