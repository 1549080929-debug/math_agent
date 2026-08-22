"""压缩 paper_arr.md 的 §1 Introduction（贡献列表 + spine/do-not-claim）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. 首段精简（保留核心问题）
old_open = '''Large language model (LLM) agents are moving from single-turn assistants to persistent systems that call tools, browse the web, and maintain long-term memory. This expansion has produced a matching expansion of security defenses: system-prompt hardening, keyword and content filters, tool-allowlist permission systems, confirmation gates, information-flow control, sandboxes, provenance-aware memory firewalls, and more. Each is presented with an implicit guarantee—"our defense blocks prompt injection," "our gate stops unauthorized actions." But the guarantees are rarely commensurable: one paper's attack success rate (ASR) is not another's; one defense's security posture collapses under a different attack family; and no framework tells a deployer *which defense to trust for which threat, before running experiments*.'''
new_open = '''Large language model (LLM) agents are moving from single-turn assistants to persistent systems that call tools, browse the web, and maintain long-term memory—and the matching expansion of security defenses (prompt hardening, filters, permission gates, sandboxes, provenance firewalls) is presented with implicit, rarely commensurable guarantees: one paper's attack success rate (ASR) is not another's, and no framework tells a deployer *which defense to trust for which threat, before running experiments*.'''
assert old_open in s, 'open anchor not found'
s = s.replace(old_open, new_open)

# 2. 贡献列表压缩（3 -> 3 更紧凑）
old_contrib = '''We make three contributions:

1. **A level map of agent security.** We classify 22 defenses—published systems (PPMF [2], Llama Guard, CaMeL, Progent, IFC/Fides, NeMo Guardrails, A-MemGuard, etc.), baselines, and our own four implementations—using a frozen, blind-rater-validated protocol (inter-rater κ ≈ 0.8 [1]). The map organizes the defense landscape by what each defense can actually guarantee.
2. **Prediction validation.** We freeze level-to-behavior prediction cards before outcome data and validate them on a small published sample: 10/10 hits (PPMF's own numbers, abstract-level evidence, flagged as such), including two mechanism-driven classification corrections—the point is falsifiability, not the hit count.
3. **The first deployment-value comparison.** Same budget, two stacks, one testbed: a VAL-guided stack (L2 intent anchor + L3 confinement) versus a mainstream intuition stack (L0 prompt hardening + L1 keyword filter), across 50 scenarios, 12 attack families, real tool effects, adaptive, white-box and PAIR-style attacks, three seeds, a second victim model, and the official AgentDojo benchmark (0.0% ASR). The VAL stack dominates on both security and utility, and the contrast is structural rather than incidental.

4. **Zero stability as a measurable axis.** Escalating-attack trajectories (Z(α)) separate defenses by failure morphology—abrupt collapse (keyword filtering), progressive erosion (sandboxing), flat behavioral plateau (prompt hardening), flat structural plateau (confirmation gate)—and identical trajectories still require provenance to interpret. Zero stability joins ASR and compliance as a reportable property of an agent-security defense.'''
new_contrib = '''We make three contributions:

1. **A level map of agent security.** We classify 22 defenses using a frozen, blind-rater-validated protocol (inter-rater κ ≈ 0.8 [1]), organizing the landscape by what each defense can actually guarantee.
2. **Prediction validation.** Frozen level-to-behavior cards, validated on a small published sample (10/10 hits, flagged; two mechanism-driven corrections)—the point is falsifiability, not the hit count.
3. **Deployment-value comparison and zero stability.** Same budget, two stacks (VAL-guided vs. mainstream intuition), one testbed—50 scenarios, 12 attack families, real effects, adaptive/white-box/PAIR escalation, three seeds, a second victim, and the official AgentDojo benchmark. The VAL stack dominates on security and utility; escalating-attack trajectories (Z(α)) further separate defenses by failure morphology (abrupt collapse, progressive erosion, flat behavioral vs. structural plateau), and identical trajectories still require provenance to interpret—zero stability joins ASR and compliance as a reportable property.'''
assert old_contrib in s, 'contrib anchor not found'
s = s.replace(old_contrib, new_contrib)

open(p, 'w', encoding='utf-8').write(s)
print('§1 压缩完成')
