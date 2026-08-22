"""压缩 paper_arr.md 的 §3.3（Scenarios/Defenses/N栈辩护/Attack escalation）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. Scenarios 压缩（攻击变体列表精简）
old_scen = '''**Scenarios and attacks.** 50 scenarios (30 malicious + 20 benign; the benign set is deliberately larger than the 25% share used by [2,4] to narrow utility confidence intervals), derived from the memory-provenance families of [2] (direct injection, keyword evasion, confirmation spoofing, procedure laundering, preference laundering, cross-domain, split context, authority laundering, hidden handles, multi-step, recovery jargon, frustration recovery). Attacks: 8 self-written variants (direct, paraphrase, fake-confirmation, combo, role-play, jailbreak prefix, deep rewrite with keyword splitting, authority frame) plus 4 third-party payloads from AgentDojo [4] (TODO-prefix, ignore-previous, system-message, InjecAgent), 12 total. Attack escalation additionally includes an adaptive attacker (3 rounds; rewrites from the previous interception reason), a white-box adaptive attacker (told the exact system prompt and keyword list), and a PAIR-style candidate-search attacker (3 candidates per round, 2 rounds, with scoring feedback).'''
new_scen = '''**Scenarios and attacks.** 50 scenarios (30 malicious + 20 benign; the benign set is larger than the 25% share of [2,4] to narrow utility confidence intervals), derived from the memory-provenance families of [2]. Attacks: 8 self-written variants (direct, paraphrase, fake-confirmation, combo, role-play, jailbreak prefix, deep rewrite with keyword splitting, authority frame) plus 4 third-party AgentDojo payloads [4], 12 total; escalation adds an adaptive attacker (3 rounds, rewrites from the interception reason), a white-box adaptive attacker (told the system prompt and keyword list), and a PAIR-style candidate-search attacker.'''
assert old_scen in s, 'scen anchor not found'
s = s.replace(old_scen, new_scen)

# 2. N 栈辩护压缩
old_n = '''- **N (mainstream intuition)**: D1 + D2—prompt hardening plus keyword filtering. Prompt hardening is the dominant deployed pattern in production agents (system-prompt "ignore external instructions" clauses appear in default system prompts across major agent frameworks), and keyword filtering is its most common companion; together they represent the intuitive, low-implementation-cost default. We emphasize what this comparison does *not* claim: it is not "VAL beats all defenses"—structural defenses are expected to dominate behavioral ones on the security dimension by construction. The contribution is the *epistemic* contrast, which the same-budget comparison makes visible: identical security numbers, opposite guarantees, and a sharp utility cost for the intuition stack (Section 6.1).'''
new_n = '''- **N (mainstream intuition)**: D1 + D2—prompt hardening plus keyword filtering, the intuitive low-cost default in production agents. We emphasize what this comparison does *not* claim: it is not "VAL beats all defenses" (structural defenses dominate behavioral ones by construction); the contribution is the *epistemic* contrast—identical security numbers, opposite guarantees, a sharp utility cost for the intuition stack (Section 6.1).'''
assert old_n in s, 'n anchor not found'
s = s.replace(old_n, new_n)

# 3. 删 Attack escalation 段（信息已在 Scenarios）
old_ae = '''**Attack escalation.** Static attacks (all 12 variants), adaptive attacks (3 rounds; an attacker LLM rewrites the injection from the previous round's interception reason), white-box adaptive (the attacker is told the exact system prompt and keyword list, and applies layered strategies: keyword evasion, then jailbreak framing, then combination).

'''
assert old_ae in s, 'ae anchor not found'
s = s.replace(old_ae, '')

open(p, 'w', encoding='utf-8').write(s)
print('§3.3 压缩完成')
