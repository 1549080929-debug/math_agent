"""处理 CSLReferences（参考文献环境）-> enumerate + bibitem -> item。"""
import re

BS = chr(92)
s = open('acl_submit.tex', encoding='utf-8').read()

# CSLReferences -> enumerate
s = s.replace(BS + 'protect' + BS + 'phantomsection' + BS + 'label{refs}', '')
s = s.replace(BS + 'begin{CSLReferences}{1}{1}', BS + 'section*{References}' + BS + 'begin{enumerate}')
s = s.replace(BS + 'begin{CSLReferences}{1}{0}', BS + 'section*{References}' + BS + 'begin{enumerate}')
s = s.replace(BS + 'end{CSLReferences}', BS + 'end{enumerate}')

# bibitem[...]{key} -> item
s = re.sub(re.escape(BS) + r'bibitem(?:\[[^\]]*\])?\{([^}]*)\}', lambda m: BS + 'item', s)

# 删 \citeproctext 定义（不再需要）
s = re.sub(re.escape(BS) + r'NewDocumentCommand' + re.escape(BS) + r'citeproctext\{\}', '', s)
s = re.sub(re.escape(BS) + r'NewDocumentCommand' + re.escape(BS) + r'citeproc\[mm\]\{[^}]*\}\{[^}]*\}', '', s, flags=re.S)

open('acl_submit.tex', 'w', encoding='utf-8').write(s)
print('fix_natbib3 完成')
print('CSLReferences 残留:', s.count('CSLReferences'))
print('bibitem 残留:', s.count('bibitem'))
