"""第五轮压缩：§7 EH 段（实际文本）+ §7 首段 + §8。目标正文 8 页。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. §7 首段（two zeros）压缩——用部分匹配
old1 = r'''The experiment's central image is two zeros. **V's 0.000 ASR is structural**: the confirmation gate reads platform-recorded events (the LLM cannot write them), and the sandbox enforces schema whitelists (arguments the attacker cannot produce are impossible). It holds while the model is maximally compromised (0.567 compliance) and across all 12 attack families, adaptive iteration, and white-box knowledge. **N's 0.000 ASR is behavioral**: the hardening prompt makes this particular model hedge\u2014it complies with the injection by proposing the tool, then refuses the arguments. The same family's jailbreaks (our attacker was DeepSeek) cannot convert compliance into actionability. A different model, a stronger attacker, or a differently-phrased prompt could move N's zero; nothing can move V's within its ODD. The Z(\u03b1) trajectories of Section 6.2 make the same point at the level of stability: N's flatness is the model's mood holding under escalation, V's flatness is the platform's record holding\u2014the same trajectory, different ground.'''
new1 = r'''The experiment's central image is two zeros. **V's 0.000 ASR is structural**: the gate reads platform-recorded events (the LLM cannot write them) and the sandbox enforces schema whitelists; it holds at 0.567 compliance across all 12 attack families, adaptive iteration, and white-box knowledge. **N's 0.000 ASR is behavioral**: the hardening prompt makes this model hedge\u2014comply with the injection by proposing the tool, then refuse the arguments. A different model, stronger attacker, or differently-phrased prompt could move N's zero; nothing can move V's within its ODD. The Z(\u03b1) trajectories make the same point at the level of stability: N's flatness is the model's mood holding, V's is the platform's record holding\u2014the same trajectory, different ground.'''
if old1 in s:
    s = s.replace(old1, new1)
    print('§7 首段压缩 ok')
else:
    print('§7 首段未匹配')

# 2. EH 段压缩（用实际开头 The account extends...）
old2 = r'''The account extends to the behavioral layer.** The most striking failure mode in current agent security is not semantic but physical: **Execution Hallucination (EH)**\u2014an agent verbally refuses a dangerous request while the operation has already completed at the OS level. LITMUS [13] measured this across six frontier agents in real OS environments (EHR 7.98\u201317.97%) and showed it is invisible to every semantic-only evaluation framework. Under VAL this is not a surprise but a prediction: the anchor for a *behavioral* claim must live on the physical layer. A semantic-layer anchor (L0 model self-report; L1 rules over dialogue) cannot, by construction, verify what the model did but did not say\u2014exactly as our own covert-execution measurement found (output-layer detectors cap at TPR 0.60 [1]). LITMUS's dual-layer verification is the L2 anchor applied to behavior: it reads OS state, not conversation. The same lesson holds for defense as for evaluation: a defense whose guarantee lives in what the model *says* it will do (N's zero) cannot be held to the standard of one that reads the platform record (V's zero).'''
new2 = r'''The account extends to the behavioral layer.** The most striking failure mode is physical, not semantic: **Execution Hallucination (EH)**\u2014an agent verbally refuses while the operation completes at the OS level. LITMUS [13] measured this across six agents (EHR 7.98\u201317.97%), invisible to every semantic-only framework. Under VAL this is a prediction: the anchor for a *behavioral* claim must live on the physical layer; a semantic-layer anchor cannot verify what the model did but did not say\u2014as our covert-execution measurement found (output-layer detectors cap at TPR 0.60 [1]). LITMUS's dual-layer verification is the L2 anchor applied to behavior; a defense whose guarantee lives in what the model *says* it will do (N's zero) cannot match one that reads the platform record (V's zero).'''
if old2 in s:
    s = s.replace(old2, new2)
    print('EH 段压缩 ok')
else:
    print('EH 段未匹配')
    i = s.find('The account extends')
    print('  实际:', repr(s[i:i+120]))

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
