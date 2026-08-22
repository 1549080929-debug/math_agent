"""压 §8 Limitations（腾空间给 Conclusion 进页 8）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

i = s.find('## 8. Limitations')
j = s.find('## 9. Conclusion')
if i < 0 or j < 0:
    print('锚点未找到')
    raise SystemExit

new8 = '''## 8. Limitations

1. **Single model (victim and attacker).** All attacks used DeepSeek-chat; cross-family attackers (Kimi, Llama 8B) declined the role. A less-aligned attacker and GCG remain open variants.
2. **Self-built testbed.** Scenarios, defenses, and sandbox are ours\\u2014deliberate for a controlled comparison; Section 6.5 validates on AgentDojo's official harness (0.0% ASR). Our behavioral blind spot (covert execution, TPR 0.60 [1]) is independently reproduced by LITMUS [13]; we did not run its harness.
3. **Coverage.** Twelve attack families plus adaptive/white-box/PAIR; token-level optimization absent; 20 benign scenarios (CIs in Section 6.1).
4. **Raters and prediction sample.** Blind-validated (security subset 90.9%, \\u03ba \\u2248 0.8 [1]); 10/10 hits on a small sample\\u2014the mechanism is the claim, not the hit count.

'''
s = s[:i] + new8 + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print('§8 压缩，字数:', len(s.split()))
