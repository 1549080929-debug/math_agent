"""把 paper.md 的数字引用 [n] 映射为 pandoc citeproc [@key]，生成 ARR 用的 LaTeX。

映射表（对应 refs.bib 的 key）。
"""
import re

NUM2KEY = {
    1: 'yin2026grading', 2: 'xu2026memory', 3: 'han2025verifiagent',
    4: 'debenedetti2024agentdojo', 5: 'injection2026dissociation',
    6: 'slr2026source', 7: 'lu2025when', 8: 'zhou2023ralm',
    9: 'inan2023llamaguard', 10: 'chen2023codet', 11: 'shi2025progent',
    12: 'costa2025ifc', 13: 'zhang2026litmus',
    14: 'amemguard2025', 15: 'camel2025',
}

s = open('paper.md', encoding='utf-8').read()

# 替换 [n]、[n, m]、[n,m] 为 [@key;@key]
def repl(m):
    nums = [int(x.strip()) for x in m.group(1).split(',')]
    keys = [NUM2KEY[n] for n in nums if n in NUM2KEY]
    if not keys:
        return m.group(0)
    return '[' + ';'.join('@' + k for k in keys) + ']'

s2 = re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', repl, s)

# 检查是否有未映射的数字引用
unmapped = re.findall(r'\[(\d+(?:\s*,\s*\d+)*)\]', s2)
if unmapped:
    print('警告：仍有数字引用（可能不在 1-13）:', unmapped[:10])

open('paper_cite.md', 'w', encoding='utf-8').write(s2)
print('已生成 paper_cite.md（引用映射为 citeproc 格式）')
