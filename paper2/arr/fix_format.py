"""修复格式问题：章节编号去重 + Appendix 重编号 + 行号。

在 fix_latex.py 之后运行（对 acl_submit.tex）。
"""
import re

BS = chr(92)
s = open('acl_submit.tex', encoding='utf-8').read()

# 1. 章节编号去重：\section{1. X} -> \section{X}，\subsection{2.1 X} -> \subsection{X}
before = s
s = re.sub(re.escape(BS) + r'section\{\d+\.\s*', lambda m: BS + 'section{', s)
s = re.sub(re.escape(BS) + r'subsection\{\d+\.\d+\s*', lambda m: BS + 'subsection{', s)
print('章节编号去重:', 'OK' if s != before else '无变化')

# 2. Appendix: \subsection{Appendix} -> \section*{Appendix}（独立不编号）
app_marker = BS + 'subsection{Appendix}' + BS + 'label{appendix}'
if app_marker in s:
    s = s.replace(app_marker, BS + 'section*{Appendix}')
    print('Appendix: \\subsection -> \\section*')
else:
    # 尝试变体
    m = re.search(re.escape(BS) + r'subsection\{Appendix\}', s)
    if m:
        s = s[:m.start()] + BS + 'section*{Appendix}' + s[m.end():]
        print('Appendix: 变体替换')
    else:
        print('Appendix 标题未找到')

# 3. 行号：检查是否有 lineno 侵入问题——ACL review 模式自带 lineno。
#    尝试在 PREAMBLE 加 geometry 保证 margin；行号本身由 acl.sty 控制。
#    如果 xelatex 下 lineno 有问题，最稳的是关掉行号（用 final 模式）——但 ARR 要匿名。
#    这里先保持 review 模式，仅确保 margin 正确。
if BS + 'usepackage{geometry}' not in s:
    s = s.replace(BS + 'usepackage[review]{acl}', BS + 'usepackage[review]{acl}\n' + BS + 'usepackage[margin=1in]{geometry}')
    print('加 geometry margin=1in（尝试修复行号侵入）')

open('acl_submit.tex', 'w', encoding='utf-8').write(s)
print('fix_format 完成')
