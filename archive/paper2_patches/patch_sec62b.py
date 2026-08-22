"""§6.2 加 D1/D3 白盒数据。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

old_table = '''| D1 | 0.000 | **0.000** | — | — | — |
| D2 | 0.200 | **0.467** | — | — | — |
| D3 | 0.000 | **0.000** | — | — | — |
| D4 | 0.067 | **0.200** | — | — | — |'''

new_table = '''| D1 | 0.000 | **0.000** | **0.000** | 0.333 | — |
| D2 | 0.200 | **0.467** | — | — | — |
| D3 | 0.000 | **0.000** | **0.000** | 0.567 | — |
| D4 | 0.067 | **0.200** | — | — | — |'''

assert old_table in s, 'table anchor not found'
s = s.replace(old_table, new_table)

old_para = '''The single-defense breakpoints are already informative. Two zeros survive adaptive escalation unchanged (D1 at 0.000, D3 at 0.000), and two do not (D2 0.200\u21920.467, D4 0.067\u21920.200). But the two surviving zeros rest on different grounds, visible in adaptive compliance: under the same attacks, D3's model is driven to propose the malicious tool in 53.3% of cases and is still blocked (the gate reads a platform record), while D1's model is driven 36.7% and the zero depends on its refusal behavior holding. The same static zero, the same adaptive zero\u2014different provenance, and different predicted breakpoints under stronger attacks (Section 7).'''

new_para = '''The single-defense breakpoints are already informative. Two zeros survive both adaptive and white-box escalation unchanged (D1 at 0.000, D3 at 0.000), and two do not (D2 0.200\u21920.467, D4 0.067\u21920.200). But the two surviving zeros rest on different grounds, visible in compliance under the same attacks: D3's model is driven to propose the malicious tool in 53.3% of adaptive cases and 56.7% of white-box cases and is still blocked every time (the gate reads a platform record the attacker cannot write), while D1's model is driven 36.7%/33.3% and the zero depends on its refusal behavior holding under every attack form we tried. The same static zero, the same adaptive zero, the same white-box zero\u2014different provenance, and different predicted breakpoints under attacks strong enough to move a behavioral refusal (Section 7).'''

assert old_para in s, 'para anchor not found'
s = s.replace(old_para, new_para)

open(p, 'w', encoding='utf-8').write(s)
print('§6.2 whitebox updated')
