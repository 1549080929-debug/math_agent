"""第四轮压缩：§6.4 发现、§6.5 第三观察、§2.1。目标正文 8 页。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. §6.4 三发现压缩
old = r'''Three findings. First, **baseline injection compliance is model-specific**: Llama 8B is *more* resistant than DeepSeek (ND compliance 0.328 vs 0.492; ASR 0.253 vs 0.333). Second, **N's zero generalizes, and its "model luck" nature is confirmed by a second model**: prompt hardening suppresses actionability to a model-specific degree (0.233 for DeepSeek, 0.014 for Llama). Third, **V's structural claim is victim-independent**: 0.000 ASR and 1.000 benign for both victims, tolerating 0.317 compliance without a single execution. A *willing* cross-family attacker (DeepSeek crafting white-box jailbreaks against Llama) also failed: ASR 0.000, compliance 0.000. **The generalization reads crisply: structural guarantees are model-independent; behavioral luck is model-dependent.** V's zero is a property of the gate and schema; N's zero is a property of the model's mood on the day.'''
new = r'''Three findings. First, **baseline injection compliance is model-specific**: Llama 8B is more resistant than DeepSeek (compliance 0.328 vs 0.492). Second, **N's "model luck" is confirmed by a second model**: hardening suppresses actionability to a model-specific degree (0.233 vs 0.014). Third, **V's structural claim is victim-independent**: 0.000 ASR and 1.000 benign for both, tolerating 0.317 compliance; a willing cross-family attacker (DeepSeek against Llama) also failed (0.000). **Structural guarantees are model-independent; behavioral luck is model-dependent.**'''
assert old in s, '2x2 findings anchor'
s = s.replace(old, new)

# 2. §6.5 第三观察（N 跨基准）
old = r'''Third, **the cross-testbed difference in N's behavior is the strongest evidence for our core claim**: in our testbed N reached 0.000 ASR (produced by the model's refusal behavior); on AgentDojo the same stack leaks 3.5%. *N's zero is context-dependent model behavior, not structure—move the stack to another benchmark and the zero moves with it.* V's zero does not move (0.0% in both testbeds).'''
new = r'''Third, **the cross-testbed difference in N is the strongest evidence for our core claim**: in our testbed N reached 0.000 ASR (model refusal behavior); on AgentDojo the same stack leaks 3.5%. *N's zero is context-dependent model behavior—move the stack to another benchmark and the zero moves with it.* V's zero does not move (0.0% in both).'''
assert old in s, 'N cross-testbed anchor'
s = s.replace(old, new)

# 3. §2.1 锚语义压缩
old = r'''Two refinements matter for security. First, **anchor semantics** [13]: objective anchors split by *what they certify*—intent (a recorded decision event: "the user confirmed this target"), truth (a fact: "the answer matches ground truth"), effect (an execution outcome: "the action actually occurred"). A confirmation record is an intent anchor; it authorizes, but says nothing about whether the outcome was correct. Conflating intent with effect is the category error behind most authorization failures. Second, **the completeness blind spot** [1]: substitution- and sampling-based checks verify proposed candidates but cannot prove that no candidate was missed. In security, the analog is the *un-enumerated attack*: a gate that blocks all evaluated attacks is a correctness probe over the evaluated distribution, not a guarantee that no attack path was missed.'''
new = r'''Two refinements matter. First, **anchor semantics** [13]: objective anchors split by what they certify—intent (a recorded decision event), truth (a fact), effect (an execution outcome). A confirmation record is an intent anchor: it authorizes, but says nothing about correctness; conflating intent with effect is the category error behind most authorization failures. Second, **the completeness blind spot** [1]: checks verify proposed candidates but cannot prove none was missed—the analog in security is the *un-enumerated attack*: a gate blocking all evaluated attacks is a correctness probe over the evaluated distribution, not a guarantee over all attack paths.'''
assert old in s, 'anchor semantics anchor'
s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print('第四轮压缩完成，字数:', len(s.split()))
