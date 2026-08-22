"""P1-2: baseline 辩护（N 栈定义 + 比较边界）。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

old = '''- **N (mainstream intuition)**: D1 + D2—prompt hardening plus keyword filtering, the most common real-world combination.'''

new = '''- **N (mainstream intuition)**: D1 + D2—prompt hardening plus keyword filtering. Prompt hardening is the dominant deployed pattern in production agents (system-prompt "ignore external instructions" clauses appear in default system prompts across major agent frameworks), and keyword filtering is its most common companion; together they represent the intuitive, low-implementation-cost default. We emphasize what this comparison does *not* claim: it is not "VAL beats all defenses"—structural defenses are expected to dominate behavioral ones on the security dimension by construction. The contribution is the *epistemic* contrast: two stacks can reach the same zero ASR with opposite guarantees, and the same-budget comparison makes the utility cost of the intuition stack visible (Section 6.1).'''

assert old in s, 'N stack anchor not found'
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('P1-2 done')
