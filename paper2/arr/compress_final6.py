"""最后一压：EH 段 + §8 合并 5/6 条。目标正文 8 页。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. EH 段压到极短
i = s.find('The account extends to the behavioral layer')
j = s.find('\n## 8. Limitations', i)
if i > 0 and j > 0:
    new_eh = '''The account extends to the behavioral layer.** **Execution Hallucination (EH)**\\u2014an agent verbally refuses while the operation completes at the OS level\\u2014was measured by LITMUS [13] across six agents (EHR 7.98\\u201317.97%), invisible to every semantic-only framework. Under VAL this is a prediction: the anchor for a *behavioral* claim must live on the physical layer; a semantic-layer anchor cannot verify what the model did but did not say (TPR 0.60 [1]).'''
    s = s[:i] + new_eh + s[j:]
    print('[ok] EH 段压到极短')

# 2. §8 合并 5/6
old = '''5. **LLM-rater classifications.** Blind-validated among same-family raters (security subset 90.9% exact, overall \\u03ba \\u2248 0.8 [1]); human-rater agreement is future work. The classifier itself is an L1 tool whose reproducibility was measured\\u2014the judge's judge, applied to the judge itself.
6. **Prediction sample.** 10/10 hits on a small, partially abstract-level sample; the mechanism (anchor \\u2192 failure mode) is the claim, not the hit count.'''
new = '''5. **Raters and prediction sample.** Blind-validated among same-family raters (security subset 90.9%, \\u03ba \\u2248 0.8 [1]); the classifier itself is an L1 tool whose reproducibility was measured. 10/10 prediction hits on a small sample; the mechanism is the claim, not the hit count.'''
if old in s:
    s = s.replace(old, new)
    print('[ok] §8 5/6 合并')
else:
    print('[warn] §8 5/6 未匹配（检查）')

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
