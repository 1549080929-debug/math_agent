"""定位落地：Abstract 措辞 + Introduction 三层结构 + do-not-claim。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

# 1. Abstract: VAL 定位为 guarantee-provenance framework + "Zero is an outcome"
old_abs = 'The same zero, two different guarantees. We further identify where L3 anchors exist in agent security:'
new_abs = ('The same zero, two different guarantees\u2014zero is an outcome, not a guarantee. '
           'VAL is a guarantee-provenance framework for LLM-agent security: it identifies what an '
           'observed security outcome is grounded in, and hence where it will fail. '
           'We further identify where L3 anchors exist in agent security:')
assert old_abs in s, 'abstract anchor not found'
s = s.replace(old_abs, new_abs)

# 2. Introduction "What this paper claims" 段重写为三层结构 + do-not-claim
old_spine = '''**What this paper claims—the spine in one paragraph.** (i) *The anchor predicts the failure mode:* every one of the 22 classified defenses fails the way its anchor fails, and we froze the predictions before the outcome data (Section 5). (ii) *The same zero is not the same guarantee:* a VAL-selected stack and a mainstream-intuition stack both reach 0.000 ASR, but one is structure and the other is model luck—visible in the compliance gap and across two victim models (Section 6). (iii) *The framework knows its own level:* the classifier used here is itself an L1 tool, and we measured rather than assumed its reproducibility (Section 8). If a reader remembers only one of these, it should be (ii).'''

new_spine = '''**What this paper claims—the spine in one paragraph.** The argument runs on three levels. *Phenomenon:* two agent-security defenses can reach the same observed zero ASR with opposite guarantees—visible in the compliance gap and across two victim models (Section 6). *Mechanism:* the difference lies in the verification anchor, i.e., where the security verdict is grounded (Section 5). *Method:* VAL provides a compact language for identifying the strongest guarantee a defense actually grounds, and predicts the failure boundary of each level. A meta-claim completes the picture: the classifier used here is itself an L1 tool, and we measured rather than assumed its reproducibility (Section 8). If a reader remembers only one sentence, it should be: *the same zero is not the same guarantee—zero is an outcome, not a guarantee.*'''

assert old_spine in s, 'spine anchor not found'
s = s.replace(old_spine, new_spine)

# 3. Introduction 末尾加 do-not-claim scoping 段
old_scope = 'If a reader remembers only one sentence, it should be: *the same zero is not the same guarantee—zero is an outcome, not a guarantee.*'
new_scope = old_scope + '''

**What we do not claim.** VAL is not a general theory of AI verification, a complete security evaluation, or a ranking of defenses by quality. It is a mid-level methodological claim about LLM-agent security: when two defenses produce the same observed security outcome, the provenance of that outcome—which verification anchor grounds it—determines its guarantee and predicts its failure boundary. Claims about robotics, formal methods, human-in-the-loop systems, or non-agentic LLMs are outside this paper's scope; so is a claim that VAL covers every possible defense. We study the question the field has not asked explicitly, within the setting where we can answer it with controlled experiments and third-party benchmarks.'''

assert old_scope in s, 'scope anchor not found'
s = s.replace(old_scope, new_scope)

open(p, 'w', encoding='utf-8').write(s)
print('定位落地 done')
