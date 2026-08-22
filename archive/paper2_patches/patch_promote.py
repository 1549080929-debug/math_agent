"""Z(α) 提升为正式贡献：Abstract + 贡献列表 + §7 呼应。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

# 1. Abstract: zero stability 句
old_abs = 'The same zero, two different guarantees\u2014zero is an outcome, not a guarantee. VAL is a guarantee-provenance framework for LLM-agent security:'
new_abs = ('The same zero, two different guarantees\u2014zero is an outcome, not a guarantee. '
           'Under escalating attacks, zero stability becomes a measurable axis: some zeros collapse abruptly, '
           'others erode gradually, and indistinguishable stability trajectories can rest on opposite '
           'guarantees (model behavior vs. platform record). '
           'VAL is a guarantee-provenance framework for LLM-agent security:')
assert old_abs in s, 'abstract anchor not found'
s = s.replace(old_abs, new_abs)

# 2. 贡献列表：加贡献 4（在贡献 3 之后、"What this paper claims" 之前）
old_c3_end = 'The VAL stack dominates on both security and utility, and the contrast is structural rather than incidental.'
new_c3_end = old_c3_end + '''

4. **Zero stability as a measurable axis.** Escalating-attack trajectories (Z(\u03b1)) separate defenses by failure morphology\u2014abrupt collapse (keyword filtering), progressive erosion (sandboxing), flat behavioral plateau (prompt hardening), flat structural plateau (confirmation gate)\u2014and identical trajectories still require provenance to interpret. Zero stability joins ASR and compliance as a reportable property of an agent-security defense.'''
assert old_c3_end in s, 'contribution 3 end not found'
s = s.replace(old_c3_end, new_c3_end)

open(p, 'w', encoding='utf-8').write(s)
print('promote patch applied')
