"""移 §6.2 自适应/白盒表到附录 A.5（正文留文字引用）。"""
import re

p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# §6.2 表（| Config | Static ASR | Adaptive ASR ...）
m = re.search(r'\| Config \| Static ASR \| Adaptive ASR \| White-box ASR \| White-box compliance \| PAIR-lite ASR \|\n\|[-| ]+\|\n(.*?)\n\n', s, re.S)
if m:
    table = m.group(0).strip()
    ai = s.find('## Appendix')
    if ai > 0:
        s = s[:ai] + s[ai:].replace('## Appendix', '## Appendix\n\n### A.5 Single-defense escalation (static/adaptive/white-box)\n\n' + table + '\n', 1)
        print('[ok] §6.2 表移附录 A.5')
    s = s[:m.start()] + 'The full escalation table is in Appendix A.5; the key contrast: D1/D3 hold at 0.000 across static/adaptive/white-box, while D2 (0.200\u21920.467) and D4 (0.067\u21920.200) leak and worsen.\n\n' + s[m.end():]
    print('[ok] 正文留引用')
else:
    print('[warn] §6.2 表未找到')

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
