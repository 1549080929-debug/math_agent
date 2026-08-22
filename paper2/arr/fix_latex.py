"""修复 acl_submit.tex：Unicode 数学符号 + longtable -> table*（正确提取列数）。"""
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

# 2. longtable -> table* + tabular（以 \toprule 分界列格式与内容）
BEG = BS + 'begin{longtable}'
END = BS + 'end{longtable}'
TOPRULE = BS + 'toprule'
n = 0
while BEG in s:
    i = s.find(BEG)
    e = s.find(END, i)
    tr = s.find(TOPRULE, i)
    if e < 0 or tr < 0 or tr > e:
        break
    # 列格式块 = BEG 后到 \toprule 前；列数 = >{\raggedright 次数
    colspec_block = s[i + len(BEG):tr]
    ncols = colspec_block.count(BS + '>{\\raggedright')
    if ncols == 0:
        ncols = max(1, colspec_block.count('p{'))
    # 表格内容 = \toprule 后到 \end{longtable} 前
    inner = s[tr + len(TOPRULE):e]
    # 清理 noalign、booktabs 命令、连续 \\
    inner = inner.replace(BS + 'noalign{}', '')
    inner = inner.replace(BS + 'toprule', BS + 'hline')
    inner = inner.replace(BS + 'midrule', BS + 'hline')
    inner = inner.replace(BS + 'bottomrule', BS + 'hline')
    # 表头 \endhead 处理
    ENDHEAD = BS + 'endhead'
    eh = inner.find(ENDHEAD)
    if eh >= 0:
        head = inner[:eh].strip()
        body = inner[eh + len(ENDHEAD):].strip()
        while head.endswith(BS + BS):
            head = head[:-2].rstrip()
        inner = head + ' ' + BS + BS + ' ' + BS + 'hline' + chr(10) + body
    # 连续 \\ 清理
    while (BS + BS + ' ' + BS + BS) in inner:
        inner = inner.replace(BS + BS + ' ' + BS + BS, BS + BS)
    while (BS + BS + BS + BS) in inner:
        inner = inner.replace(BS + BS + BS + BS, BS + BS)
    # \hline 重复清理
    hh = BS + 'hline' + BS + 'hline'
    while hh in inner:
        inner = inner.replace(hh, BS + 'hline')
    # 去掉 \endfirsthead/\endfoot/\endlastfoot/\caption/\label
    for cmd in ['endfirsthead', 'endfoot', 'endlastfoot']:
        c = BS + cmd
        while c in inner:
            p = inner.find(c)
            inner = inner[:p] + inner[p + len(c):]
    inner = re.sub(re.escape(BS) + r'caption\{[^}]*\}', '', inner)
    inner = re.sub(re.escape(BS) + r'label\{[^}]*\}', '', inner)
    inner = inner.strip()

    colspec_new = 'l' * ncols
    repl = (BS + 'begin{table*}[!t]' + chr(10) + BS + 'centering' + chr(10) + BS + 'small' + chr(10)
            + BS + 'begin{tabular}{' + colspec_new + '}' + chr(10) + inner + chr(10)
            + BS + 'end{tabular}' + chr(10) + BS + 'end{table*}' + chr(10))
    s = s[:i] + repl + s[e + len(END):]
    n += 1

print(f'longtable 转换: {n} 个')
open('acl_submit.tex', 'w', encoding='utf-8').write(s)
print('修复完成')
