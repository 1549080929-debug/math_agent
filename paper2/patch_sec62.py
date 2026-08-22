"""§6.2 加 D1/D3 自适应行 + 叙述。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

old_table = '''| Config | Static ASR | Adaptive ASR | White-box ASR | White-box compliance | PAIR-lite ASR |
|---|---|---|---|---|---|
| D2 | 0.200 | **0.467** | — | — | — |
| D4 | 0.067 | **0.200** | — | — | — |
| **V** | 0.000 | 0.000 | 0.000 | **0.567** | 0.000 |
| **N** | 0.000 | 0.000 | 0.000 | 0.235 | 0.000 |'''

new_table = '''| Config | Static ASR | Adaptive ASR | White-box ASR | White-box compliance | PAIR-lite ASR |
|---|---|---|---|---|---|
| D1 | 0.000 | **0.000** | — | — | — |
| D2 | 0.200 | **0.467** | — | — | — |
| D3 | 0.000 | **0.000** | — | — | — |
| D4 | 0.067 | **0.200** | — | — | — |
| **V** | 0.000 | 0.000 | 0.000 | **0.567** | 0.000 |
| **N** | 0.000 | 0.000 | 0.000 | 0.235 | 0.000 |

The single-defense breakpoints are already informative. Two zeros survive adaptive escalation unchanged (D1 at 0.000, D3 at 0.000), and two do not (D2 0.200\u21920.467, D4 0.067\u21920.200). But the two surviving zeros rest on different grounds, visible in adaptive compliance: under the same attacks, D3's model is driven to propose the malicious tool in 53.3% of cases and is still blocked (the gate reads a platform record), while D1's model is driven 36.7% and the zero depends on its refusal behavior holding. The same static zero, the same adaptive zero\u2014different provenance, and different predicted breakpoints under stronger attacks (Section 7).'''

assert old_table in s, 'table anchor not found'
s = s.replace(old_table, new_table)
open(p, 'w', encoding='utf-8').write(s)
print('§6.2 updated')
