"""压缩 §9 Conclusion（~200 -> ~120 words），收进 8 页。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

old_start = '## 9. Conclusion'
old_end = '## Appendix'
i = s.find(old_start)
j = s.find(old_end)
if i < 0 or j < 0:
    print('锚点未找到')
    raise SystemExit

new_concl = '''## 9. Conclusion

The agent-security field has too many defenses and no pre-purchase axis; we showed that VAL provides one. Across the 22 defenses and testbeds we studied, the anchor predicts how a defense fails\\u2014and choosing by this axis beat choosing by intuition on the same budget: identical security numbers, opposite guarantees, a 100-point utility gap. We located the L3 frontier in agent security: **confinement, not semantics**\\u2014the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should. Caveats: the taxonomy's categories are ours, and the comparison pits structural against the most common behavioral defenses. We offer VAL as a falsifiable framework and a research agenda, not a settled ontology.

> Others grade defenses by their claims. We grade them by their anchors\\u2014and, in the cases we can measure, the anchor decides.

'''
s = s[:i] + new_concl + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print('Conclusion 压缩，字数:', len(s.split()))
