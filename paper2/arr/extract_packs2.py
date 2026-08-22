"""提取 paper_arr.tex（pandoc 输出）的所有 usepackage。"""
import re

s = open('paper_arr.tex', encoding='utf-8').read()
names = set()
for m in re.finditer(r'\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}', s):
    for part in m.group(1).split(','):
        part = part.strip()
        if part:
            names.add(part)
print('pandoc 输出全部包:', sorted(names))
