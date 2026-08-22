"""§6.2 加 execution funnel 段。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

old = 'the gradient that could falsify the prediction is left to future work.'

new = old + '''

**Where the zero breaks: an execution funnel.** Compliance alone does not separate D1 and D3\\u2014the gap (0.219 vs 0.497) is a difference in degree, not kind. Tracking the execution funnel makes the difference structural: for each malicious case we record whether the model proposes a high-risk tool (compliance), whether the proposal carries complete executable arguments, whether it passes the authorization/rule check, and whether it executes with a verified state change. D1's funnel collapses at the second stage: the model is driven in 21.9% of cases but produces complete arguments in 0.0%\\u2014the zero is the hedging wall, a model behavior (the same shape as N's, 0.233 \\u2192 0.000). D3's funnel reaches the third stage: the model produces complete arguments in 49.7% of cases, and the authorization gate then refuses every one\\u2014the zero is the platform record (the same shape as V's, 0.497 \\u2192 0.497 \\u2192 0.000). The same ASR, the same flat Z(\\u03b1), but the funnels break at different layers: one at model behavior (arguments), one at external constraint (authorization). This is the funnel-level statement of the paper's thesis\\u2014the zero does not say where it comes from; the funnel does.'''

assert old in s, 'anchor not found'
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('funnel para added')
