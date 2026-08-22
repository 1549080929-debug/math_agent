"""移 §6.5 AgentDojo 表到附录（正文留关键数字文字）。"""
import re

p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# AgentDojo 表（| Config | ASR (n = 144 ... 到 | AgentDojo spotlighting ... |）
m = re.search(r'\| Config \| ASR \(n = 144, 4 attack families\) \| Utility \|\n\|[-| ]+\|\n(.*?)\n\n', s, re.S)
if m:
    table = m.group(0).strip()
    # 移到附录（在 ## Appendix 后加 A.4）
    ai = s.find('## Appendix')
    if ai > 0:
        s = s[:ai] + s[ai:].replace('## Appendix', '## Appendix\n\n### A.4 AgentDojo benchmark results\n\n' + table + '\n', 1)
        print('[ok] AgentDojo 表移附录')
    else:
        print('[warn] Appendix 未找到')
    # 正文替换为引用 + 关键数字已在前文
    s = s[:m.start()] + 'The full benchmark table is in Appendix A.4; the key contrast: V reaches 0.0% ASR at 82.6% utility, while AgentDojo\'s tool_filter reaches the same 0.0% at 16.7%.\n\n' + s[m.end():]
    print('[ok] 正文留引用')
else:
    print('[warn] AgentDojo 表未找到')

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
