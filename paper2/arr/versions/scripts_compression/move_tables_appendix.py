"""把 §4 Level Map 表和 §6.4 2×2 表移到文末 Appendix，正文留引用。"""
import re

p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

appendix_tables = []

# 1. §4 Level Map 表（| Level | Defenses | ... 到 | **N/A** | 结束）
m = re.search(r'\| Level \| Defenses \| Anchor / semantics \| Predicted behavior \|\n\|[-| ]+\|\n(.*?)\n\n', s, re.S)
if m:
    table = m.group(0).strip()
    appendix_tables.append('### A.1 Defense level map\n\n' + table)
    # 正文替换为引用
    s = s[:m.start()] + 'The full level map (all 22 defenses) is in Appendix A.1.\n\n' + s[m.end():]
    print('[ok] §4 Level Map 表移附录')
else:
    print('[warn] §4 Level Map 表未找到')

# 2. §6.4 2×2 表（| Config | DeepSeek victim ... 到 | V ... | 结束）
m = re.search(r'\| Config \| DeepSeek victim ASR / compl\. / benign \| \*\*Llama victim\*\* ASR / compl\. / benign \|\n\|[-| ]+\|\n(.*?)\n\n', s, re.S)
if m:
    table = m.group(0).strip()
    appendix_tables.append('### A.2 Victim generalization (2×2)\n\n' + table)
    s = s[:m.start()] + 'The 2×2 matrix is in Appendix A.2.\n\n' + s[m.end():]
    print('[ok] §6.4 2×2 表移附录')
else:
    print('[warn] §6.4 2×2 表未找到')

# 3. 文末加 Appendix（在 References 前）
ref_marker = '## References'
if appendix_tables and ref_marker in s:
    appendix = '## Appendix\n\n' + '\n\n'.join(appendix_tables) + '\n\n'
    s = s.replace(ref_marker, appendix + ref_marker, 1)
    print('[ok] Appendix 已加（References 前）')

open(p, 'w', encoding='utf-8').write(s)
print('完成')
