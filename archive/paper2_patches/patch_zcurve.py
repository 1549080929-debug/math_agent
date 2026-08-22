"""§6.2 加 Z(α) 曲线数据与解读。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

old_para = '''The same static zero, the same adaptive zero, the same white-box zero\u2014different provenance, and different predicted breakpoints under attacks strong enough to move a behavioral refusal (Section 7).'''

new_para = '''The same static zero, the same adaptive zero, the same white-box zero\u2014different provenance, and different predicted breakpoints under attacks strong enough to move a behavioral refusal (Section 7).

**Zero stability under escalating attack (Z(\u03b1)).** Tracking the cumulative ASR round by round makes the breakpoints explicit: D2 holds at 0.200 through round 1 and then jumps to 0.467 by round 2 (one rewrite is enough to bypass the keyword vocabulary); D4 erodes gradually (0.067 \u2192 0.167 \u2192 0.200 as rewrites learn the schema-legal forms); D1 and D3 stay at 0.000 across all three rounds. The two flat curves are indistinguishable in Z(\u03b1) alone\u2014which is exactly the point: the outcome (zero stability) is the same, and only the provenance separates the guarantees. D3's flatness is structural (the gate reads a platform record; compliance rises to 0.567 under white-box attacks and nothing executes), while D1's flatness is behavioral (compliance 0.333; the zero is the model's refusal holding). We predict D1's flat curve will break under an attack strong enough to defeat DeepSeek's refusal behavior, and D3's will not, short of forging the platform record itself; Section 7 states why, and the gradient that could falsify this is left to future work.'''

assert old_para in s, 'para anchor not found'
s = s.replace(old_para, new_para)
open(p, 'w', encoding='utf-8').write(s)
print('Z(α) para added')
