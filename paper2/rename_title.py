"""批量更新论文标题引用：The Anchor Decides -> The Same Zero。"""
import io
import os

OLD_FULL = "The Anchor Decides: Verification Autonomy Levels Predict the Success of LLM-Agent Security Defenses"
NEW_FULL = "The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security"
OLD_SHORT = "The Anchor Decides"
NEW_SHORT = "The Same Zero"

files = [
    r"paper2\paper.md",
    r"paper2\submission.md",
    r"README.md",
    r"HANDOFF.md",
    r"docs\15-方向3综合：VAL预测安全防御.md",
    r"docs\17-2027投稿规划.md",
    r"docs\20-致南航LITMUS团队信.md",
    r"promo\arxiv-paper2-walkthrough.md",
]

for f in files:
    if not os.path.exists(f):
        print(f'  [跳过] {f} (不存在)')
        continue
    s = open(f, encoding='utf-8').read()
    orig = s
    s = s.replace(OLD_FULL, NEW_FULL)
    s = s.replace(OLD_SHORT, NEW_SHORT)
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)
        print(f'  [更新] {f}')
    else:
        print(f'  [无匹配] {f}')
