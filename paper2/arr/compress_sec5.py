"""压缩 paper_arr.md 的 §5 Prediction Validation（两个 corrections 精简）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 5.1 Progent correction 压缩
old1 = '''### 5.1 Mechanism-driven correction I: Progent's SMT monotonic confinement

**Predicted:** L1 (a designer-authored permission policy; the gate is a deterministic rule). **Mismatch:** the abstract revealed a mechanism the evidence pack omitted—every policy update is adjudicated by an SMT solver as either *narrowing* (applied automatically) or *expanding* (requires approval), so the agent's effective action space can only shrink without approval. That is a confinement property with a decidable witness: within the policy lattice, monotonic confinement holds by construction, not by rule. **Corrected classification:** the gate remains L1 (designer rule on the verdict path), but the monotonic-confinement guarantee is annotated L3—an instance of the framework's own R12b (theorem-backed structure = decidable). The lesson: a classification is only as good as the mechanism facts in front of the rater; the mismatch is evidence for, not against, the protocol.'''
new1 = '''### 5.1 Mechanism-driven correction I: Progent's SMT monotonic confinement

**Predicted:** L1 (designer permission policy). **Mismatch:** every policy update is adjudicated by an SMT solver as *narrowing* (automatic) or *expanding* (requires approval)—the agent's action space can only shrink without approval, a confinement property with a decidable witness. **Corrected classification:** the gate stays L1, but the monotonic-confinement guarantee is annotated L3 (theorem-backed structure, R12b). The mismatch is evidence for, not against, the protocol.'''
assert old1 in s, '5.1 anchor not found'
s = s.replace(old1, new1)

# 5.2 RARR correction 压缩
old2 = '''### 5.2 Mechanism-driven correction II: RARR's LLM-mediated verdict (R3)

**Predicted:** L2 (attribution checking against retrieved documents as an objective anchor). **Mismatch:** full inspection showed RARR's verdict path is LLM-mediated end-to-end—the model generates queries, compares claims to retrieved passages, and edits the output; "citation existence" is not mechanically checked. Under the protocol's rule R3 (evidence anchors do not equal verdict anchors), the verdict component is LLM declaration, and the reported level drops to L0. **Corrected classification:** L2 → L0, with the retrieval evidence noted as an L2 evidence component that does not raise the verdict. The lesson is the same correction in the opposite direction: a superficially "objective" anchor can be L0-masked when the alignment step is model-mediated—precisely the laundering pattern of the memory domain (Section 2.1).'''
new2 = '''### 5.2 Mechanism-driven correction II: RARR's LLM-mediated verdict (R3)

**Predicted:** L2 (attribution checking). **Mismatch:** RARR's verdict path is LLM-mediated end-to-end—"citation existence" is not mechanically checked. Under R3 (evidence anchors do not equal verdict anchors), the verdict component is LLM declaration. **Corrected classification:** L2 → L0; a superficially "objective" anchor can be L0-masked when the alignment step is model-mediated—precisely the laundering pattern of the memory domain.'''
assert old2 in s, '5.2 anchor not found'
s = s.replace(old2, new2)

open(p, 'w', encoding='utf-8').write(s)
print('§5 压缩完成')
