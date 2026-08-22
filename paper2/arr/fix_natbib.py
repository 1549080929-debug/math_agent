"""给 thebibliography 的 \\bibitem 加编号 label，消除 natbib author-year 警告。"""
import re

BS = chr(92)
s = open('acl_submit.tex', encoding='utf-8').read()

# thebibliography 内的 \bibitem{key} -> \bibitem[n]{key}
n = 0
def repl(m):
    global n
    n += 1
    return BS + 'bibitem[' + str(n) + ']{' + m.group(1) + '}'

# 只在 thebibliography 范围内替换
start = s.find(BS + 'begin{thebibliography}')
end = s.find(BS + 'end{thebibliography}')
if start > 0 and end > 0:
    bib = s[start:end]
    bib2 = re.sub(re.escape(BS) + r'bibitem\{([^}]*)\}', repl, bib)
    s = s[:start] + bib2 + s[end:]
    print(f'natbib: {n} 条 \\bibitem 加 label')
else:
    print('thebibliography 未找到')

open('acl_submit.tex', 'w', encoding='utf-8').write(s)
