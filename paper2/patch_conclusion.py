"""P0-2: 软化结论 headline claim。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

old_concl = '''The agent-security field has a deployment problem: too many defenses, no pre-purchase axis. We showed that VAL provides one. The anchor of a defense predicts how it fails—text rules fail to rewriting, model self-assessment fails to compliance, objective anchors fail outside their ODD, and structural anchors (confinement, information flow, data-control separation) hold by construction within it. We measured that choosing by this axis beats choosing by intuition on the same budget: identical security numbers, opposite guarantees, and a 100-point utility gap. And we located the L3 frontier in agent security: **confinement, not semantics**—the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should.'''

new_concl = '''The agent-security field has a deployment problem: too many defenses, no pre-purchase axis. We showed that VAL provides one. Across the 22 defenses, attack families, and testbeds we studied, the anchor of a defense predicts how it fails—text rules fail to rewriting, model self-assessment fails to compliance, objective anchors fail outside their ODD, and structural anchors (confinement, information flow, data-control separation) hold by construction within it. In our controlled same-budget comparison, choosing by this axis beat choosing by intuition: identical security numbers, opposite guarantees, and a 100-point utility gap. We also located the L3 frontier in agent security: **confinement, not semantics**—the properties worth encoding into decidable systems are the ones that restrict what an agent can do, not the ones that judge whether it should. Two caveats bound these claims: the taxonomy's categories are ours (validated by blind-rater agreement and out-of-sample predictions, not by an external ground truth), and the deployment comparison pits structural defenses against the most common behavioral defenses, not against every defense in the landscape. We offer VAL as a falsifiable framework and a research agenda—not as a settled ontology.'''

assert old_concl in s, 'conclusion anchor not found'
s = s.replace(old_concl, new_concl)

old_slogan = '> Others grade defenses by their claims. We grade them by their anchors—and the anchor decides.'
new_slogan = '> Others grade defenses by their claims. We grade them by their anchors—and, in the cases we can measure, the anchor decides.'
assert old_slogan in s, 'slogan anchor not found'
s = s.replace(old_slogan, new_slogan)

open(p, 'w', encoding='utf-8').write(s)
print('P0-2 done')
