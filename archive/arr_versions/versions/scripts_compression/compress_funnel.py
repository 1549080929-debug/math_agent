"""funnel 段压缩（匹配字面量 \\u2014/\\u03b1）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 用字面量版本（\\u2014 是文件里的 6 字符）
old = r'''**Where the zero breaks: an execution funnel under static attacks.** The funnel is a mechanism snapshot at one attack condition (static, 12 variants, n=360)\u2014it is not the 7-round Z(\u03b1) trajectory, which is reported separately above. For each malicious case we record whether the model proposes a high-risk tool (compliance), whether the proposal carries complete executable arguments, whether it passes the authorization/rule check, and whether it executes with a verified state change. D1's funnel collapses at the second stage: the observed zero is terminated at the complete-argument stage\u2014the model fails to produce executable arguments under the hardening prompt. The break is at parameter completeness, but the anchor remains behavioral: D1 contains no structural parameter-integrity verifier; argument completeness is whatever the model happens to produce (the same shape as N's, 0.233 \u2192 0.000). D3's funnel reaches the third stage: the model produces complete arguments in 49.7% of cases, and the authorization gate then refuses every one\u2014the zero is the platform record (the same shape as V's, 0.497 \u2192 0.497 \u2192 0.000). The same ASR, the same flat Z(\u03b1), but the funnels break at different layers: one at model behavior (arguments), one at external constraint (authorization). This is the funnel-level statement of the paper's thesis\u2014the zero does not say where it comes from; the funnel does.'''

new = r'''**Where the zero breaks: an execution funnel under static attacks** (a mechanism snapshot, distinct from the 7-round Z(\u03b1) above). For each case we record whether the model proposes a high-risk tool (compliance), whether the proposal carries complete arguments, and whether it passes authorization and executes with a verified state change. D1's funnel collapses at the second stage: the zero is terminated at the complete-argument stage\u2014the model fails to produce executable arguments under the hardening prompt. The break is at parameter completeness, but the anchor remains behavioral: D1 has no structural parameter-integrity verifier (same shape as N's, 0.233 \u2192 0.000). D3's funnel reaches the third stage: complete arguments in 49.7% of cases, refused every time by the authorization gate\u2014the zero is the platform record (same shape as V's, 0.497 \u2192 0.497 \u2192 0.000). The same ASR and flat Z(\u03b1), but the funnels break at different layers: model behavior (arguments) vs. external constraint (authorization). The zero does not say where it comes from; the funnel does.'''

if old in s:
    s = s.replace(old, new)
    print('funnel 段压缩完成')
else:
    print('[warn] funnel 段未匹配，检查前 100 字符')
    i = s.find('Where the zero breaks')
    print(repr(s[i:i+100]))

open(p, 'w', encoding='utf-8').write(s)
