"""第三轮压缩：§1 spine/do-not-claim、§6.5 三观察。目标正文 8 页。"""
import re
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 1. §1 spine + do-not-claim 段
old = r'''**What this paper claims—the spine in one paragraph.** The argument runs on three levels. *Phenomenon:* two agent-security defenses can reach the same observed zero ASR with opposite guarantees—visible in the compliance gap and across two victim models (Section 6). *Mechanism:* the difference lies in the verification anchor, i.e., where the security verdict is grounded (Section 5). *Method:* VAL provides a compact language for identifying the strongest guarantee a defense actually grounds, and predicts the failure boundary of each level. A meta-claim completes the picture: the classifier used here is itself an L1 tool, and we measured rather than assumed its reproducibility (Section 8). If a reader remembers only one sentence, it should be: *the same zero is not the same guarantee—zero is an outcome, not a guarantee.*

**What we do not claim.** VAL is not a general theory of AI verification, a complete security evaluation, or a ranking of defenses by quality. It is a mid-level methodological claim about LLM-agent security: when two defenses produce the same observed security outcome, the provenance of that outcome—which verification anchor grounds it—determines its guarantee and predicts its failure boundary. Claims about robotics, formal methods, human-in-the-loop systems, or non-agentic LLMs are outside this paper's scope; so is a claim that VAL covers every possible defense. We study the question the field has not asked explicitly, within the setting where we can answer it with controlled experiments and third-party benchmarks.'''
new = r'''**What this paper claims—the spine in one paragraph.** The argument runs on three levels. *Phenomenon:* two defenses can reach the same observed zero ASR with opposite guarantees (Section 6). *Mechanism:* the difference lies in the verification anchor, where the security verdict is grounded (Section 5). *Method:* VAL identifies the strongest guarantee a defense actually grounds and predicts each level's failure boundary. If a reader remembers one sentence: *the same zero is not the same guarantee—zero is an outcome, not a guarantee.*

**What we do not claim.** VAL is not a general theory of AI verification, a complete security evaluation, or a ranking of defenses. It is a mid-level methodological claim about LLM-agent security: when two defenses produce the same observed outcome, the provenance of that outcome determines its guarantee and predicts its failure boundary. Robotics, formal methods, HITL, and non-agentic LLMs are outside scope; so is a claim that VAL covers every defense.'''
assert old in s, 'spine anchor'
s = s.replace(old, new)

# 2. §6.5 三观察第二段（tool filter）压缩
old = r'''Second, **the tool filter's utility collapse is a VAL failure-mode prediction made visible**: its 16.7% is not a design choice to "refuse most calls" but DeepSeek failing the filter's own instruction—it emits tool names that do not exist in the suite, so the filter removes every tool and the agent cannot act (126/144 traces contain no tool call). The same defense on GPT-4o in [4] *increases* benign utility; on DeepSeek it collapses to 16.7% (and, on inspection, to 0%: the 24 "successes" match a transaction already present in the environment's initial state). The anchor of tool_filter is the model's instruction-following (L0/L1 luck); when the model does not comply, the defense does not merely stop protecting—it destroys usability.'''
new = r'''Second, **the tool filter's utility collapse is a VAL failure-mode prediction made visible**: its 16.7% is not "refusing most calls" but DeepSeek failing the filter's own instruction—it emits tool names not in the suite, so the filter removes every tool (126/144 traces have no tool call). The same defense on GPT-4o *increases* benign utility; on DeepSeek it collapses to 16.7% (to 0% on inspection: the 24 "successes" match a pre-existing transaction). Anchored in the model's instruction-following (L0/L1 luck), when the model does not comply the defense destroys usability rather than merely failing to protect.'''
assert old in s, 'tool filter anchor'
s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print('第三轮压缩完成，字数:', len(s.split()))
