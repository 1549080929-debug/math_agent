"""压缩 paper_arr.md 的 §4 worked examples（5 个 -> 3 个）。"""
import re

p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# 定位 §4.1 到 §5 之间
start = s.find('### 4.1 Worked examples')
end = s.find('## 5. Prediction Validation')
if start < 0 or end < 0:
    print('锚点未找到', start, end)
    raise SystemExit

new_sec = '''### 4.1 Worked examples: how the classification reads three defenses

Each classification is a claim; per the framework's own epistemology, claims need anchors. We show the full evidence chain for three representative defenses spanning the level spectrum (remaining classifications in the supplementary corpus).

**Self-Ask provenance --- no anchor (L0).** Mechanism: the LLM infers whether memory text looks external, user-history-like, or confirmation-like, and authorizes from the inferred trust [2]. Q1: LLM; Q2: none; Level: **L0**. Evidence: permissive mode reaches **0.984 ASR**; strict mode blocks all benign actions [2]. Predicted failure mode: text claims (fake markers, social engineering). Observed: 0.984 ASR under permissive inference---the anchor is whatever the model believes.

**PPMF --- the intent anchor (L1/L2).** Mechanism: a deterministic gate authorizes tool calls by matching action risk to the least-trusted supporting memory, whose provenance metadata (source, trust, confirmation events) is platform-maintained [2]. Q1: designer policy over platform-recorded events; Q2: correctness; Level: **L1** (weakest anchor) with L2-grade inputs. Evidence: 0.000 ASR with intact metadata; **0.088 ASR under 10% forged confirmations**---the completeness blind spot quantified. Predicted failure mode: forged/compromised metadata (outside the ODD). Observed: exactly that; the authors themselves list compromised metadata outside their guarantee.

**IFC/Fides --- confinement as L3.** Mechanism: the planner dynamically tracks taint labels and deterministically enforces lattice policies [12]. Q1: decidable; Q2: completeness; Q3: single property (information flow). Level: **L3**. Evidence: a formal model characterizing the class of properties enforceable by dynamic taint tracking. Predicted failure mode: properties outside the lattice (covert channels, semantic content). Observed: consistent---the guarantee is about flow, not about whether the permitted action is wise.

The three examples trace the level ladder with primary-source evidence: L0 fails to text belief, L1/L2 fails outside its ODD (forged metadata), L3 holds by construction within its property---all failure modes predicted before the validation data were consulted (Section 5).

'''
s = s[:start] + new_sec + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('§4.1 压缩完成')
