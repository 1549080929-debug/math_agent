"""修复 acl_submit.tex：Unicode 数学符号 + longtable -> table*（纯字符串，避开正则转义）。"""
import re

BS = chr(92)

UNI_MAP = {
    'α': '$\\alpha$', 'β': '$\\beta$', 'κ': '$\\kappa$',
    '≈': '$\\approx$', '×': '$\\times$', '→': '$\\rightarrow$', '≤': '$\\leq$',
    '≥': '$\\geq$', '±': '$\\pm$', '∈': '$\\in$', 'σ': '$\\sigma$',
    'μ': '$\\mu$', 'Δ': '$\\Delta$', 'γ': '$\\gamma$', 'π': '$\\pi$',
    '–': '--', '—': '---',
}

s = open('acl_submit.tex', encoding='utf-8').read()

# 1. Unicode 替换
for u, latex in UNI_MAP.items():
    s = s.replace(u, latex)

# 2. longtable -> table* + tabular
BEG = BS + 'begin{longtable}'
END = BS + 'end{longtable}'
ENDHEAD = BS + 'endhead'
n = 0
while BEG in s:
    i = s.find(BEG)
    j = s.find('{', i + len(BEG))
    if j < 0:
        break
    k = s.find('}', j)
    colspec = s[j + 1:k]
    e = s.find(END, k)
    if e < 0:
        break
    inner = s[k + 1:e]
    # 表头：\endhead 前是表头行（保留），后是表体
    eh = inner.find(ENDHEAD)
    if eh >= 0:
        head = inner[:eh].strip()
        body = inner[eh + len(ENDHEAD):].strip()
        # 去掉 head 末尾的 \\（后面会补 \\ \hline）
        while head.endswith(BS + BS):
            head = head[:-2].rstrip()
        inner = head + ' ' + BS + BS + ' ' + BS + 'hline\n' + body
    # 清理连续 \\（\\ \\ 或 \\\\ -> \\），表格行分隔只保留一个
    while (BS + BS + ' ' + BS + BS) in inner:
        inner = inner.replace(BS + BS + ' ' + BS + BS, BS + BS)
    while (BS + BS + BS + BS) in inner:
        inner = inner.replace(BS + BS + BS + BS, BS + BS)
    # 去掉可能的 \endfirsthead/\endfoot/\endlastfoot/\caption/\label/\noalign
    for cmd in ['endfirsthead', 'endfoot', 'endlastfoot']:
        c = BS + cmd
        while c in inner:
            p = inner.find(c)
            inner = inner[:p] + inner[p + len(c):]
    inner = re.sub(r'\\caption\{[^}]*\}', '', inner)
    inner = re.sub(r'\\label\{[^}]*\}', '', inner)
    inner = inner.replace(BS + 'noalign{}', '')
    inner = inner.replace(BS + 'toprule', BS + 'hline')
    inner = inner.replace(BS + 'midrule', BS + 'hline')
    inner = inner.replace(BS + 'bottomrule', BS + 'hline')
    # 清理 \hline \\ \hline 等冲突（表头转换产生的）
    inner = inner.replace(BS + 'hline' + ' ' + BS + BS + ' ' + BS + 'hline', BS + BS + ' ' + BS + 'hline')
    inner = inner.replace(BS + 'hline' + BS + BS + BS + 'hline', BS + BS + BS + 'hline')
    # \hline \hline -> \hline（字符串替换，避免正则转义）
    hh = BS + 'hline' + BS + 'hline'
    while hh in inner:
        inner = inner.replace(hh, BS + 'hline')
    inner = inner.strip()
    # 简化列格式：去 >{...} 前缀，p{...} 保留（minipage 内容保留）
    colspec = re.sub(r'>\{[^}]*\}', '', colspec)
    repl = (BS + 'begin{table*}[!t]\n' + BS + 'centering\n' + BS + 'small\n'
            + BS + 'begin{tabular}{' + colspec + '}\n' + inner + '\n'
            + BS + 'end{tabular}\n' + BS + 'end{table*}\n')
    s = s[:i] + repl + s[e + len(END):]
    n += 1

print(f'longtable 转换: {n} 个')

# 行级清理：行首孤立 \\（如 "\\ \\hline" 行）——表格表头残留
out_lines = []
for line in s.split('\n'):
    st = line.strip()
    if st in (BS + BS + ' ' + BS + 'hline', BS + BS + BS + 'hline', BS + BS):
        # 行首孤立 \\（无前导内容）：去掉
        st = st.replace(BS + BS, '').strip()
        if st:
            out_lines.append(' ' * (len(line) - len(line.lstrip())) + st)
        continue
    out_lines.append(line)
s = '\n'.join(out_lines)

# 3. CSLReferences 使用处 -> thebibliography（绕开 CSL 环境坑）
s = s.replace(BS + 'begin{CSLReferences}{1}{0}', BS + 'begin{thebibliography}{9}')
s = s.replace(BS + 'begin{CSLReferences}{1}{1}', BS + 'begin{thebibliography}{9}')
s = s.replace(BS + 'end{CSLReferences}', BS + 'end{thebibliography}')
# natbib 兼容：\bibitem[\citeproctext]{key} -> \bibitem{key}
s = s.replace(BS + 'bibitem[' + BS + 'citeproctext]{', BS + 'bibitem{')

open('acl_submit.tex', 'w', encoding='utf-8').write(s)
print('修复完成')
