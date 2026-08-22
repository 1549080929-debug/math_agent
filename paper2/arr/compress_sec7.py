"""压缩 paper_arr.md 的 §7（deployment answer 段）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

old = '''This is the deployment answer to "which defense should I buy?": **VAL selection buys a guarantee; intuition buys the model's current mood.** The cost difference is visible in the same table: both reach zero, but N's zero costs every benign action (0.000 benign success—users cannot transfer rent or send reports), while V's zero is lossless. The official tool filter on AgentDojo (§6.5) is the same story from the other side: a defense whose anchor is the model's instruction-following does not merely fail to protect when the model does not comply—it *destroys usability* (utility 16.7%, and 0% once the false-positive task is removed). Under VAL's usage criteria ([1], cost of silent error × encodability), the deployer's question becomes precise: *is the threat inside the anchor's ODD?* If yes, L2/L3 structure is available; if no, the honest answer is L2 correctness plus labeling, not a claim of safety.'''
new = '''This is the deployment answer to "which defense should I buy?": **VAL selection buys a guarantee; intuition buys the model's current mood.** Both reach zero, but N's zero costs every benign action (0.000 benign success) while V's is lossless; the AgentDojo tool filter (§6.5) is the same story from the other side—a defense anchored in the model's instruction-following *destroys usability* when the model does not comply. Under VAL's usage criteria ([1]), the deployer's question becomes precise: *is the threat inside the anchor's ODD?* If yes, L2/L3 structure is available; if no, the honest answer is L2 correctness plus labeling, not a claim of safety.'''
assert old in s, 'sec7 anchor not found'
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('§7 压缩完成')
