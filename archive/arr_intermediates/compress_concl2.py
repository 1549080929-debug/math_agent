"""压缩 Conclusion 到极短（收进页 8）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

i = s.find('## 9. Conclusion')
j = s.find('## Appendix')
if i < 0 or j < 0:
    print('锚点未找到')
    raise SystemExit

new = '''## 9. Conclusion

The agent-security field has too many defenses and no pre-purchase axis; we showed that VAL provides one. The anchor predicts how a defense fails\\u2014and choosing by this axis beat intuition on the same budget: identical security numbers, opposite guarantees, a 100-point utility gap. We located the L3 frontier in agent security: **confinement, not semantics**\\u2014encode what restricts what an agent can do, not what judges whether it should. We offer VAL as a falsifiable framework and a research agenda, not a settled ontology.

'''
s = s[:i] + new + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print('Conclusion 极短压缩，字数:', len(s.split()))
