"""提取 acl_submit.tex 引用的所有 LaTeX 包（简单字符串解析）。"""
import re

s = open('acl_submit.tex', encoding='utf-8').read()
names = set()
# 找所有 \usepackage{...} 和 \usepackage[...]{...}
for m in re.finditer(r'\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}', s):
    for part in m.group(1).split(','):
        part = part.strip()
        if part:
            names.add(part)
for m in re.finditer(r'\\RequirePackage(?:\[[^\]]*\])?\{([^}]*)\}', s):
    for part in m.group(1).split(','):
        part = part.strip()
        if part:
            names.add(part)
print('需要的包:', sorted(names))
