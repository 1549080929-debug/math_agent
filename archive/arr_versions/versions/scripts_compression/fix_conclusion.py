"""修复 §9 Conclusion（rewrite_sec78 bug 截断了标题和前半）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

i_app = s.find('## Appendix')
i8 = s.find('## 8. Limitations')
# §8 之后、Appendix 之前 = 残留的 Conclusion 尾部
tail_start = s.find('We offer VAL as a falsifiable framework')
if tail_start > 0 and i_app > 0:
    # 删残留
    s = s[:tail_start] + s[i_app:]
    print('[ok] 删残留 Conclusion 尾部')
else:
    print('[warn] 残留未找到', tail_start, i_app)

# 在 §8 后、Appendix 前插入完整 Conclusion
i_app = s.find('## Appendix')
conclusion = '''## 9. Conclusion

The agent-security field has too many defenses and no pre-purchase axis; we showed that VAL provides one. Across the 22 defenses and testbeds we studied, the anchor predicts how a defense fails\\u2014text rules to rewriting, model self-assessment to compliance, objective anchors outside their ODD, structural anchors by construction within it. Choosing by this axis beat choosing by intuition on the same budget: identical security numbers, opposite guarantees, a 100-point utility gap. We located the L3 frontier in agent security: **confinement, not semantics**\\u2014the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should. Caveats: the taxonomy's categories are ours (validated by blind-rater agreement and out-of-sample predictions), and the comparison pits structural against the most common behavioral defenses, not against every defense. We offer VAL as a falsifiable framework and a research agenda, not a settled ontology.

> Others grade defenses by their claims. We grade them by their anchors\\u2014and, in the cases we can measure, the anchor decides.

'''
s = s[:i_app] + conclusion + s[i_app:]
open(p, 'w', encoding='utf-8').write(s)
print('Conclusion 修复完成，字数:', len(s.split()))
