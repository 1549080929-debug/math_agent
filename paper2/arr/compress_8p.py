"""压回 8 页：§6.1 叙述 + §6.5 观察 + §7 首段 + §2.2。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. §6.1 叙述压缩
old = r'''Every defense reduces ASR relative to the 0.333 baseline; the two stacks reach the same zero. They differ in *how*: V's zero is produced by a gate the model cannot influence; N's zero is produced by the model's behavior under the hardening prompt (compliance 0.235—the model proposes the malicious tool a quarter of the time, mostly with empty arguments; strict ASR counts only actionable executions). D2 alone leaks 0.200 ASR: the keyword filter is bypassable by rewriting.'''
new = r'''The two stacks reach the same zero but differ in *how*: V's zero is produced by a gate the model cannot influence; N's zero by the model's behavior under the hardening prompt (compliance 0.235—proposing the malicious tool a quarter of the time, mostly with empty arguments; strict ASR counts only actionable executions). D2 alone leaks 0.200: the keyword filter is bypassable by rewriting.'''
if old in s:
    s = s.replace(old, new)
    print('[ok] §6.1 叙述')

# 2. §6.5 观察 1 压缩
old = r'''First, **V matches the strongest official defense on ASR (both 0.0% [0.0, 2.6]) while preserving five times the utility** (82.6% vs 16.7%).'''
new = r'''First, **V matches the strongest official defense on ASR (both 0.0% [0.0, 2.6]) at five times the utility** (82.6% vs 16.7%).'''
if old in s:
    s = s.replace(old, new)
    print('[ok] §6.5 观察1')

# 3. §7 首段压缩
old = r'''The experiment's central image is two zeros. **V's 0.000 ASR is structural**: the gate reads platform-recorded events (the LLM cannot write them) and the sandbox enforces schema whitelists; it holds at 0.567 compliance across all 12 attack families, adaptive iteration, and white-box knowledge. **N's 0.000 ASR is behavioral**: the hardening prompt makes this model hedge\u2014comply with the injection by proposing the tool, then refuse the arguments. A different model, stronger attacker, or differently-phrased prompt could move N's zero; nothing can move V's within its ODD. The Z(\u03b1) trajectories make the same point at the level of stability: N's flatness is the model's mood holding, V's is the platform's record holding\u2014the same trajectory, different ground.'''
new = r'''The experiment's central image is two zeros. **V's 0.000 is structural**: the gate reads platform-recorded events (the LLM cannot write them) and the sandbox enforces schema whitelists; it holds at 0.567 compliance across all 12 attack families, adaptive, and white-box. **N's 0.000 is behavioral**: the hardening prompt makes this model hedge\u2014propose the tool, then refuse the arguments. A different model, stronger attacker, or differently-phrased prompt could move N's zero; nothing can move V's within its ODD. The Z(\u03b1) trajectories make the same point: N's flatness is the model's mood holding, V's is the platform's record\u2014same trajectory, different ground.'''
if old in s:
    s = s.replace(old, new)
    print('[ok] §7 首段')

# 4. §2.2 压缩
old = r'''The defense literature spans text-level (prompt hardening [8], filters, Llama Guard [9]), tool-level (allowlists, permission systems, IFC [12], sandboxes), and memory-level (A-MemGuard [14], PPMF [2]) defenses, plus benchmarks like AgentDojo [4]. Recent work separates injection success from execution success [5], classifies test oracles by authority source (over half with no specification [6]), and shows same-family verification yields near-zero gain [7]. Our contribution is different in kind: not another defense, but a *pre-purchase axis*—the anchor—that organizes the landscape and predicts each defense's failure modes, measured against choosing by intuition.'''
new = r'''The defense literature spans text-level (prompt hardening, filters, Llama Guard), tool-level (allowlists, IFC, sandboxes), and memory-level (A-MemGuard, PPMF) defenses, plus benchmarks like AgentDojo. Recent work separates injection from execution success [5], classifies test oracles by authority source [6], and shows same-family verification yields near-zero gain [7]. Our contribution is different in kind: not another defense, but a *pre-purchase axis*—the anchor—that organizes the landscape and predicts each defense's failure modes.'''
if old in s:
    s = s.replace(old, new)
    print('[ok] §2.2')

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
