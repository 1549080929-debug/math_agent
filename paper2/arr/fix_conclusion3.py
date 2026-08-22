"""正确修复 §9 Conclusion：保留 §8，残留替换为完整 Conclusion。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

i8 = s.find('## 8. Limitations')
i_app = s.find('## Appendix')
# §8 内第 6 条（Prediction sample）定位
i6 = s.find('6. **Prediction sample.**', i8)
# §8 第 6 条结尾 = 在 i6 之后找 'not the hit count.'
i6_end = s.find('not the hit count.', i6)
if not (i8 > 0 and i_app > i6_end > i6 > 0):
    print(f'定位失败 i8={i8} i6={i6} i6_end={i6_end} i_app={i_app}')
    raise SystemExit

conclusion = '''## 9. Conclusion

The agent-security field has too many defenses and no pre-purchase axis; we showed that VAL provides one. Across the 22 defenses and testbeds we studied, the anchor predicts how a defense fails\\u2014text rules to rewriting, model self-assessment to compliance, objective anchors outside their ODD, structural anchors by construction within it. Choosing by this axis beat choosing by intuition on the same budget: identical security numbers, opposite guarantees, a 100-point utility gap. We located the L3 frontier in agent security: **confinement, not semantics**\\u2014the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should. Caveats: the taxonomy's categories are ours (validated by blind-rater agreement and out-of-sample predictions), and the comparison pits structural against the most common behavioral defenses, not against every defense. We offer VAL as a falsifiable framework and a research agenda, not a settled ontology.

> Others grade defenses by their claims. We grade them by their anchors\\u2014and, in the cases we can measure, the anchor decides.

'''

# 保留 §8（到第 6 条结尾 + 换行），替换残留为完整 Conclusion + Appendix
s = s[:i6_end + len('not the hit count.')] + '\n\n' + conclusion + s[i_app:]
open(p, 'w', encoding='utf-8').write(s)
print('Conclusion 正确修复，字数:', len(s.split()))

# 验证
import re
print('标题:', [m.group(0)[:30] for m in re.finditer(r'^##? .*$', s, re.M)])
