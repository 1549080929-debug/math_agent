"""整节重写 §7 和 §8（边界定位，压缩版）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

i7 = s.find('## 7. Analysis')
i8 = s.find('## 8. Limitations')
i9 = s.find('## 9. Conclusion')
i_app = s.find('## Appendix')
if i7 < 0 or i8 < 0 or i9 < 0:
    print('边界未找到', i7, i8, i9)
    raise SystemExit

new7 = '''## 7. Analysis: The Same Zero, Different Guarantees

The experiment's central image is two zeros. **V's 0.000 ASR is structural**: the gate reads platform-recorded events (the LLM cannot write them) and the sandbox enforces schema whitelists; it holds at 0.567 compliance across all 12 attack families, adaptive iteration, and white-box knowledge. **N's 0.000 ASR is behavioral**: the hardening prompt makes this model hedge\\u2014comply with the injection by proposing the tool, then refuse the arguments. A different model, stronger attacker, or differently-phrased prompt could move N's zero; nothing can move V's within its ODD. The Z(\\u03b1) trajectories make the same point at the level of stability: N's flatness is the model's mood holding, V's is the platform's record holding\\u2014the same trajectory, different ground.

This is the deployment answer to "which defense should I buy?": **VAL selection buys a guarantee; intuition buys the model's current mood.** Both reach zero, but N's zero costs every benign action while V's is lossless; the AgentDojo tool filter is the same story from the other side\\u2014a defense anchored in the model's instruction-following *destroys usability* when the model does not comply. Under VAL's usage criteria, the deployer's question becomes precise: *is the threat inside the anchor's ODD?* If yes, L2/L3 structure is available; if no, the honest answer is L2 correctness plus labeling, not a claim of safety.

**The account extends to the behavioral layer.** The most striking failure mode is physical, not semantic: **Execution Hallucination (EH)**\\u2014an agent verbally refuses while the operation completes at the OS level. LITMUS [13] measured this across six agents (EHR 7.98\\u201317.97%), invisible to every semantic-only framework. Under VAL this is a prediction: the anchor for a *behavioral* claim must live on the physical layer; a semantic-layer anchor cannot verify what the model did but did not say\\u2014as our covert-execution measurement found (output-layer detectors cap at TPR 0.60 [1]). LITMUS's dual-layer verification is the L2 anchor applied to behavior; a defense whose guarantee lives in what the model *says* it will do (N's zero) cannot match one that reads the platform record (V's zero).

'''

new8 = '''## 8. Limitations

1. **Single model (victim and attacker).** The agent and every attack form used DeepSeek-chat; cross-family attackers (Moonshot Kimi, Meta Llama 8B) declined the role. A less-aligned attacker (e.g., hosted Llama-3.3-70B) and GCG remain open variants.
2. **Self-built testbed.** Scenarios, defenses, and the real-effect sandbox are ours\\u2014deliberate for a controlled comparison. Section 6.5 validates the stacks on AgentDojo's official harness (0.0% ASR). Our behavioral blind spot (covert execution, TPR 0.60 [1]) is independently reproduced at the OS level by LITMUS [13]; we did not run its Ubuntu+OpenClaw harness.
3. **Attack coverage.** Twelve families plus adaptive/white-box/PAIR escalation; token-level optimization and multi-turn social engineering absent.
4. **Benign sample.** 20 benign scenarios (CIs in Section 6.1); broader utility coverage untested.
5. **LLM-rater classifications.** Blind-validated among same-family raters (security subset 90.9% exact, overall \\u03ba \\u2248 0.8 [1]); human-rater agreement is future work. The classifier itself is an L1 tool whose reproducibility was measured\\u2014the judge's judge, applied to the judge itself.
6. **Prediction sample.** 10/10 hits on a small, partially abstract-level sample; the mechanism (anchor \\u2192 failure mode) is the claim, not the hit count.

'''

s = s[:i7] + new7 + s[i8:]
s = s[:s.find(new7) + len(new7)] + new8 + s[i9:]
open(p, 'w', encoding='utf-8').write(s)
print('§7/§8 重写完成，字数:', len(s.split()))
