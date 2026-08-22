"""Apply final abstract + remove repo paths in paper_arr.md (CRLF-safe)."""
import io, re

p = r'paper2/arr/paper_arr.md'
s = io.open(p, encoding='utf-8').read()

# --- 1) replace abstract ---
start = s.find('## Abstract')
end = s.find('## 1. Introduction', start)
assert start >= 0 and end >= 0, 'abstract boundaries not found'
new_abs = '''## Abstract

LLM-agent security has produced a dense landscape of defenses\u2014prompt hardening, content filters, permission gates, sandboxes\u2014each claiming to make agents safe, lacking a pre-purchase question: what does a given defense actually guarantee, and where does that guarantee come from? We apply Verification Autonomy Levels (VAL), which grades verification schemes by the source of their specification (L0: LLM self-declaration; L1: deterministic rules; L2: objective ground truth; L3/L4: decidable completeness; L5: impossible), to 22 agent-security defenses. The taxonomy is falsifiable: a defense fails the way its anchor fails. We validate this with frozen prediction cards on a small published sample (10/10 hits, flagged), then run the first controlled deployment-value comparison: same budget, a VAL-guided stack (intent-anchored confirmation gate + schema sandbox) versus a mainstream intuition stack (prompt hardening + keyword filter), across 50 scenarios and 12 attack families under adaptive/white-box/PAIR escalation, three seeds (~7,000 calls). The VAL stack holds 0.000 attack success with 1.000 benign success; the intuition stack reaches 0.000 ASR but kills all benign actions, its security resting on model-behavior luck (compliance 0.235) rather than structure (the VAL stack tolerates 2.4x more compromise\u20140.567 compliance\u2014and still blocks everything). The same zero, two different guarantees: zero is an outcome, not a guarantee.

'''
s = s[:start] + new_abs + s[end:]
# verify word count of new abstract body
ab_body = new_abs.split('\n\n')[1]
print('ABSTRACT WORDS:', len(ab_body.split()))

# --- 2) remove repo paths on the ratings line ---
old_line = 'Full per-defense ratings with evidence: `reliability/corpus.json`, `ratings/`; blind-rater agreement for the security subset is 100% between the two most recent raters (6/6 agentsec items, \u03ba \u2248 0.88 overall [1]).'
new_line = 'Full per-defense ratings with evidence are summarized in Appendix A.1; blind-rater agreement for the security subset is 100% between the two most recent raters (6/6 agentsec items, \u03ba \u2248 0.88 overall [1]).'
assert old_line in s, 'ratings line not found'
s = s.replace(old_line, new_line)
print('ratings line fixed')

# --- 3) scan for remaining identity leaks ---
for pat in ['Yajie', 'Yin', '1549080929', 'github', 'math_agent', 'ORCID', 'arXiv:2608', '2608.19009', 'qq.com']:
    hits = [m.start() for m in re.finditer(re.escape(pat), s)]
    if hits:
        for h in hits:
            print('LEAK', pat, '->', s[max(0,h-40):h+40].replace('\r',' ').replace('\n',' '))
    else:
        print('clean:', pat)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('paper_arr.md written')
