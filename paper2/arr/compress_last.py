"""最后一压：§7 EH 段 + §8 Limitations。目标正文 8 页。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. EH 段压缩（当前版本）
i = s.find('The account extends to the behavioral layer')
if i > 0:
    j = s.find('\n\n## 8. Limitations', i)
    if j < 0:
        j = s.find('\n## 8. Limitations', i)
    if j > 0:
        new_eh = '''The account extends to the behavioral layer.** The most striking failure mode is physical, not semantic: **Execution Hallucination (EH)**\\u2014an agent verbally refuses while the operation completes at the OS level. LITMUS [13] measured this across six agents (EHR 7.98\\u201317.97%), invisible to every semantic-only framework. Under VAL this is a prediction: the anchor for a *behavioral* claim must live on the physical layer; a semantic-layer anchor cannot verify what the model did but did not say\\u2014as our covert-execution measurement found (TPR 0.60 [1]).'''
        s = s[:i] + new_eh + s[j:]
        print('[ok] EH 段压缩')
    else:
        print('[warn] §8 边界未找到')
else:
    print('[warn] EH 段未找到')

# 2. §8 Limitations 压缩（合并几条）
old8 = '''3. **Attack coverage.** Twelve families plus adaptive/white-box/PAIR escalation; token-level optimization and multi-turn social engineering absent.
4. **Benign sample.** 20 benign scenarios (CIs in Section 6.1); broader utility coverage untested.'''
new8 = '''3. **Coverage.** Twelve attack families plus adaptive/white-box/PAIR escalation; token-level optimization and multi-turn social engineering absent; 20 benign scenarios (CIs in Section 6.1).'''
if old8 in s:
    s = s.replace(old8, new8)
    print('[ok] §8 3-4 合并')

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
