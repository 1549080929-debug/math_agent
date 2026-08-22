"""压缩 paper_arr.md 的 §8 Limitations。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

start = s.find('## 8. Limitations')
end = s.find('## 9. Conclusion')
if start < 0 or end < 0:
    print('锚点未找到', start, end)
    raise SystemExit

new_sec = '''## 8. Limitations

1. **Single model (victim and attacker).** The agent and every attack form used DeepSeek-chat; cross-family attackers (Moonshot Kimi, Meta Llama 8B) declined the role---explicit refusals, sanitizing rewrites. A less-aligned attacker (e.g., hosted Llama-3.3-70B) and gradient-based attacks (GCG, no gradients via API) remain open variants.
2. **Self-built testbed.** Scenarios, defenses, and the real-effect sandbox are ours---deliberate for a controlled comparison of selection strategies. Section 6.5 validates the stacks on AgentDojo's official harness (their tasks, attacks, evaluation), reaching 0.0% ASR. Our behavioral blind spot (covert execution, TPR 0.60 [1]) is independently reproduced at the OS level by LITMUS [13]; we did not run its Ubuntu+OpenClaw harness---the corroboration is at the level of the structural claim.
3. **Attack coverage.** Twelve families plus adaptive/white-box/PAIR escalation; token-level optimization and multi-turn social engineering absent.
4. **Benign sample.** 20 benign scenarios (CIs in Section 6.1); broader utility coverage (long-horizon tasks) untested.
5. **LLM-rater classifications.** Blind-validated among same-family raters (security subset 90.9% exact, overall \u03ba \u2248 0.8 [1]); human-rater agreement is future work. The classifier itself is an L1 tool whose reproducibility was measured, not assumed---the judge's judge, applied to the judge itself.
6. **Prediction sample.** 10/10 hits on a small, partially abstract-level sample; the mechanism (anchor \u2192 failure mode) is the claim, not the hit count.

'''
s = s[:start] + new_sec + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('§8 压缩完成')
