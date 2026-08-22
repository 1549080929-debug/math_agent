"""修 geometry 冲突 + thebibliography -> enumerate（绕开 natbib）。"""
import re

BS = chr(92)
s = open('acl_submit.tex', encoding='utf-8').read()

# 1. 删 my geometry（acl 已加载，冲突）
s = s.replace(BS + 'usepackage[margin=1in]{geometry}', '')
print('geometry removed:', 'usepackage[margin=1in]{geometry}' not in s)

# 2. thebibliography -> section*{References} + enumerate
s = s.replace(BS + 'begin{thebibliography}{9}', BS + 'section*{References}' + BS + 'begin{enumerate}')
s = s.replace(BS + 'end{thebibliography}', BS + 'end{enumerate}')

# 3. bibitem[n]{key} -> item
s = re.sub(re.escape(BS) + r'bibitem\[\d+\]\{([^}]*)\}', lambda m: BS + 'item', s)
print('bibitem -> item 完成')

open('acl_submit.tex', 'w', encoding='utf-8').write(s)
print('fix_natbib2 完成')
